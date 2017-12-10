from abc import ABCMeta, abstractmethod
import os, re
import threading
import time
import logging
import subprocess
import copy
import socket
from queue import Empty, Queue
from collections.abc import Mapping
from ipaddress import ip_network, ip_address
from itertools import chain
from math import ceil

from taskgen.optimization import Optimization
from taskgen.taskset import TaskSet
from taskgen.live import AbstractLiveHandler, DefaultLiveHandler

# we need some conventions, to ensure that the Distributor is working
class AbstractSession(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, host, port):
        pass
    
    @abstractmethod
    def start(self, optimization, taskset):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def live_request(self):
        pass

    @abstractmethod
    def close(self):
        pass

# GenodeSession depends on AbstractSession...
from taskgen.sessions.genode import GenodeSession


class Distributor:
    
    def __init__(self,
                 destinations,
                 port=3001,
                 session=GenodeSession,
                 rescan = True,
                 max_starter = 20,
                 max_duration = 60,
                 max_ping = 4):

        if not isinstance(port, int):
            raise TypeError("port must be int")

        if not issubclass(session, AbstractSession):
            raise TypeError("session must be subtype of AbstractSession")

        self._sessions = {}
        self._starter = []
        self._port = port
        self._session = session
        self.logger = logging.getLogger('Distributor')
        self._running = threading.Event()
        self._restart_counter = 0
        self._closing = threading.Event()
        self._max_starter = max_starter
        self._max_duration = max_duration
        self._max_ping = max_ping
        self._rescan = rescan

        # build pool of IP destination addresses
        self._pool = Queue()
        if isinstance(destinations, str):
            self._append_pool(destinations)
        elif isinstance(destinations, list):
            for destination in destinations:
                self._append_pool(destination)
        else:
            raise TypeError("destinations must be [str] or str.")

        # initialize pinging and connecting of destinations
        self._init_pool()
        
        
    def _append_pool(self, destination):
        # try to parse as single ip address
        try:
            ip = ip_address(destination)
            self._pool.put(str(ip))
            return
        except ValueError:
            pass
        # parse as ip range or raise error
        for ip in ip_network(destination).hosts():
            self._pool.put(str(ip))


    def _init_pool(self):
        # calculate number of starter threads
        size = self._pool.qsize()
        duration = size * self._max_ping
        count =  duration / self._max_duration
        count = ceil(min(self._max_starter, count))
        self.logger.info("Start {} thread(s) for pinging".format(count))
        for c in range(0, count):
            starter = _Starter(self)
            starter.start()
            self._starter.append(starter)

    def _append_session(self, host):
        session = _WrapperSession(host, self)
        session.start()
        self._sessions[host] = session
        
    def start(self, taskset, optimization=None, live_handler =
              DefaultLiveHandler(), wait=True):
        
        if optimization is not None:
            if not isinstance(optimization, Optimization):
                raise TypeError("optimization must be of type Optimization")
                
        if not isinstance(live_handler, AbstractLiveHandler):
            raise TypeError("live_handler must be of type AbstractLiveHandler")
    
        if taskset is None or not isinstance(taskset, TaskSet):
            raise TypeError("taskset must be TaskSet.")

        # wrap tasksets into an threadsafe iterator
        self._tasksets = _TaskSetQueue(taskset.variants())
        self._optimization = optimization
        self._live_handler = live_handler
                
        # lets inform the single sessions about their new work
        self._restart_counter += 1
        self._running.set()
        self.logger.info("Start processing taskset")
        if wait: self.wait_finished()

    def stop(self, wait=True):
        self._running.clear()
        self.logger.info("Stop processing taskset")
        if wait: self.wait_stopped()
        
    def close(self, wait=True):
        self._closing.set()
        self.logger.info("Closing connections...")
        if wait: self.wait_closed()

    def wait_closed(self):
        self.logger.info("Waiting until ping threads are stopped")
        for starter in self._starter:
            starter.join()
            
        self.logger.info("Waiting until sessions are closed")
        for session in self._sessions.values():
            session.join()
        
    def wait_stopped(self):
        self.logger.info("Waiting until session processings are stopped")
        for session in self._sessions.values():
            session.wait_stopped()

    def wait_finished(self):
        while not self._closing.is_set():
            if self._tasksets.empty():
                break
            time.sleep(1)

            
class _TaskSetQueue():
    """Takes an iterator/generator and makes it thread-safe by
    serializing call to the `next` method of given iterator/generator.
    """
    def __init__(self, iterator):
        self.it = iterator
        self.lock = threading.Lock()
        self.queue = Queue(maxsize=1000)
        self.in_progress = 0
        self.processed = 0
        self.logger = logging.getLogger("Distributor")
        
    def get(self):
        # return a regular taskset
        with self.lock:
            if not self.queue.empty():
                try:
                    taskset = self.queue.get_nowait()
                    self.in_progress += 1
                    return taskset
                except Queue.Empty:
                    # ups, another distributor just stole our taskset
                    pass

            taskset = self.it.__next__()
            self.in_progress += 1
            return taskset
            
    def empty(self):
        with self.lock:
            # in progress?
            if self.in_progress > 0:
                return False
            # in queue?
            if not self.queue.empty():
                return False
            # in iterator?
            try:
                self.queue.put(self.it.__next__())
                return False
            except StopIteration:
                return True

    def done(self):
        with self.lock:
            self.in_progress -= 1
            self.processed += 1
            self.logger.info("{} taskset variant(s) processed".format(self.processed))
        
    def put(self, taskset):
        with self.lock:
            try:
                self.queue.put_nowait(taskset)
                self.in_progress -= 1
            except Queue.Full:
                # We don't care about the missed taskset. Actually, there is a bigger
                # problem:
                self.logger.critical("The Push-Back Queue of tasksets is full. This is a"
                    + "indicator, that the underlying session is buggy"
                    + " and is always canceling currently processed tasksets.")

            


# tries to be quiet.
# * only debug information or critical messages
class _WrapperSession(threading.Thread):
    
    def __init__ (self, host, multi):
        super().__init__()
        self._host = host
        self._multi = multi
        self.logger = logging.getLogger("Distributor({})".format(host))
        self._restart_counter = 0
        self._taskset = None
        # thread-safe is not required, but we use the wait/notify feature
        self._running = False

    def _internal_stop(self):
        self._session.stop()
        if self._taskset is not None:
            self._multi._live_handler.__taskset_stop__(self._taskset)
        self._multi._tasksets.put(self._taskset)
        self._tasket = None
        self._running = False

    def wait_stopped(self):
        while self._running:
            if self._multi._closing.wait(1):
                return
            
    def _should_restart(self):
        return (self._multi._restart_counter != self._restart_counter and
                self._should_run())

    def _should_close(self):
        return self._multi._closing.is_set()

    def _should_run(self):
        return self._multi._running.is_set()
    
    def _internal_start(self):
        try:
            # pull taskset from queue and execute it.
            self._taskset = self._multi._tasksets.get()
            self._session.start(self._taskset, self._multi._optimization)
            self._multi._live_handler.__taskset_start__(self._taskset)
            self.logger.debug("Taskset variant processing started.")
            self._restart_counter = self._multi._restart_counter
            self._running = True
            return True
        except StopIteration:
            # all tasksets are processed
            self.logger.debug("All taskset variants are processed")
            self._running = False
            return False

    def _internal_live_request(self):
        # measure the time
        timestamp = time.clock()

        # requesting & handling callback
        live_request = self._session.live_request()
        is_running = self._multi._live_handler.__handle_request__(self._taskset,
                                                                  live_request)
        if not is_running:
            self._multi._live_handler.__taskset_finish__(self._taskset)
            self._multi._tasksets.done()  # notify about the finished taskset
            self.logger.debug("Taskset variant is successfully processed")
        else:
            # do some waiting
            delay = self._multi._live_handler.__get_delay__()
            left = delay*1000 - (time.clock()-timestamp)
            if left < 0:
                self.logger.critical("Callback takes more time than espected. Live"
                                + " Request is delayed by {} ms.".format(-left))
            else:
                time.sleep(left/1000)

        return is_running
            
    def run(self):
        # try to connect
        try:
            self._session = self._multi._session(self._host, self._multi._port)
            self.logger.info("Connection established.")
        except socket.error as e:
            self.logger.critical(e)
            self._multi._pool.put(self._host)
            return 

        try:
            while not self._should_close():
                # stopping
                if not self._should_run() and self._running:
                    self._internal_stop()

                # restart or still running
                if self._should_restart() or self._running:
                    # try to start next taskset
                    if not self._internal_start():
                        continue

                    # live requests
                    while not self._should_close() and not self._should_restart():
                        # returns False, if taskset is finished. leave the loop.
                        if not self._internal_live_request():
                            break

                # idle
                elif not self._running:
                    time.sleep(0.1)

                else:
                    time.sleep(1)
                    self.logger.critical("Reached some unknown state")

            self._internal_stop()
        except socket.error as e:
            self.logger.critical(e)
            
            self.logger.debug("Taskset variant is pushed back to queue due to" +
                             " a critical error")
            if self._taskset is not None:
                self._multi._tasksets.put(self._taskset)

            # notify live handler about the stop.
            self._multi._live_handler.__taskset_stop__(self._taskset)
            
        finally:
            self._session.close()
            # push host back in pool
            self._multi._pool.put(self._host)

            
class _Starter(threading.Thread):

    def __init__(self, multi):
        super().__init__()
        self._multi = multi
        self.logger = logging.getLogger("Distributor")

    def _ping(self, host):
#        self.logger.debug("Start pinging {}".format(host))
        
        received_packages = re.compile(r"(\d) received")
        ping_out = os.popen("ping -q -W {} -c2 {}".format(self._multi._max_ping,
                                                          host),"r")
        while not self._multi._closing.is_set():
            line = ping_out.readline()
            if not line:
                break
            n_received = re.findall(received_packages,line)
            if n_received:
                return int(n_received[0]) > 0
                
    def run(self):
        while not self._multi._closing.is_set():
            try:
                host = self._multi._pool.get(True, 2) # block for 2 seconds
                if self._ping(host):
                    # try to connect
                    self.logger.info("Found {}".format(host))
                    self._multi._append_session(host)
                else:
                    # put back to pool
                    self._multi._pool.put(host)
            except Empty:
                pass
                    
            if not self._multi._rescan:
                return
