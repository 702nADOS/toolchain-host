"""
.. module:: useful_1
   :platform: Unix, Windows
   :synopsis: A useful module indeed.

.. moduleauthor:: Andrew Carter <andrew@invalid.com>


"""

import os, re
import threading
import time
import logging
import subprocess
import copy
import socket
from queue import Queue
from collections.abc import Mapping
from ipaddress import ip_network
from itertools import chain

from taskgen.distributors.simple_distributor import SimpleDistributor
from taskgen.distributor import AbstractDistributor
from taskgen.optimization import Optimization
from taskgen.taskset import TaskSet
from taskgen.live import AbstractLiveHandler, LiveResult


# die eierlegende Wohlmilchsau
class MultiDistributor:
    def __init__(self, hosts, port, ping=True, distributor_class=SimpleDistributor):
        self._live_handler = None
        self.logger = logging.getLogger('MultiDistributor')
        if isinstance(hosts, str):
            hosts = [hosts]
        elif isinstance(hosts, list) and all(isinstance(h, str) for h in hosts):
            pass
        else:
            raise TypeError("hosts must be [str] or str.")
        
        if not isinstance(port, int):
            raise TypeError("port must be int")

        if not issubclass(distributor_class, AbstractDistributor):
            raise TypeError("distributor_class must be subtype of AbstractDistributor")

        # unpack all ip addresses from range definitions
        hosts_all = []
        for host in hosts:
            hosts_all += ip_network(host).hosts()

        self._distributors = {}
        for host in hosts:
            # start one thread per host
            self._distributors[host] = _ThreadedWrapperDistributor(
                str(host),
                port,
                ping,
                distributor_class)

    @property
    def live_handler(self):
        return self._live_handler

    @live_handler.setter
    def live_handler(self, live_handler):
        if live_handler is not None:
            if not isinstance(live_handler, AbstractLiveHandler):
                raise TypeError("live_handler must be subtype of AbstractLiveHandler")
        self._live_handler = live_handler

    def start(self, taskset, optimization=None, wait=True):
        if optimization is not None:
            if not isinstance(optimization, Optimization):
                raise TypeError("optimization must be of type Optimization")
            else:
                # to prevent later changes at the opimization structure, do a full copy
                # of the object
                optimization = copy.deepcopy(optimization)

        if taskset is None or not isinstance(taskset, TaskSet):
            raise TypeError("taskset must be TaskSet.")

        # wrap tasksets into an threadsafe iterator
        tasksets = _PushBackIterator(taskset.variants())

        # lets inform the single distributors about their new work
        for distributor in self._distributors.values():
            distributor.start(tasksets, optimization)
        self.logger.debug("all distributor instances are starting.")
        if wait:
            self.logger.info("waiting until all tasksets are processed.")
            self.wait_stopping()

    def stop(self, wait=True):
        for distributor in self._distributors.values():
            distributor.stop()
        self.logger.info("all distributor instances are stopping.")
        if wait:
            self.logger.info("waiting until all distributor instances are stopped.")
            self.wait_stopping()
        
    def close(self, wait=True):        
        for distributor in self._distributors.values():
            distributor.close()
        self.logger.debug("all distributor instances are closing.")
        if wait:
            self.logger.info("waiting until all distributor instances are closed")
            self.wait_closing()
            
    def is_running(self):
        return any(d.is_running() for d in self._distributors.values())
            
    def is_closed(self):
        return any(d.is_alive() for d in self._distributors.values())

    def wait_closing(self):
        for d in self._distributors.values():
            d.join()

    def wait_stopping(self):
        for d in self._distributors.values():
            d.wait_stopping()

    def states(self):
        return iter(map(lambda x: x.state(), self._distributors.values()))


class _PushBackIterator():
    """Takes an iterator/generator and makes it thread-safe by
    serializing call to the `next` method of given iterator/generator.
    """
    def __init__(self, it):
        self.it = it
        self.lock = threading.Lock()
        self.queue = Queue(maxsize=1000)

    def __iter__(self):
        return self
            
    def __next__(self):
        if not self.queue.empty():
            try:
                return self.queue.get_nowait()
            except Queue.Empty:
                # ups, another distributor just stole our taskset
                pass

        # return a regular taskset
        with self.lock:
            return self.it.__next__()

    def put(self, taskset):
        try:
            self.queue.put_nowait(taskset)
        except Queue.Full:
            # We don't care about the missed taskset. Actually, there is a bigger
            # problem.
            logging("The Push-Back Queue of tasksets is full. This is a"
                    + "indicator, that the underlying distributor is buggy"
                    + " and is always canceling currently processed tasksets.")

class _ThreadedWrapperDistributor(threading.Thread):
    # DO NOT USE THIS CLASS. It is threaded and some attributes are not
    # thread-safe! This is a internal class for MultiDistributor
    
    
    def __init__ (self, host, port, ping=True, distributor_class=AbstractDistributor):
        super().__init__()
        # all commands are stored in this queue and processed by the thread. No
        # method of SimpleThreadedDistributor will be blocking. The Queue is
        # infinite.
        self._tasksets = None
        self._optimiziation = None  # do not alter. not thread-safe!
        self.live_handler = None
        self._distributor_class = distributor_class
        self._ping = ping
        self._processed_tasksets = 0
        self._host = host
        self._port = port
        self.logger = logging.getLogger(host)

        # thread-safe is not required, but we use the wait/notify feature
        self._pinging = threading.Event()
        self._running = threading.Event()
        self._idle = threading.Event()
        self._not_found = threading.Event()
        
        # triggers from other threads
        self._stopping = threading.Event()
        self._starting = threading.Event()
        self._closing = threading.Event()

        # start the thread immediately
        super().start()

    def state(self):
        return {
            'processed_tasksets' : self._processed_tasksets,
            'state' : {
                'idle' : self._idle.is_set(),
                'starting' : self._starting.is_set(),
                'running' : self._running.is_set(),
                'stopping' : self._stopping.is_set(),
                'closing' : self._closing.is_set(),
                'closed' : not self.is_alive(),
                'pinging' : self._pinging.is_set()
            }
        }
    
    def start(self, tasksets, optimization=None):
        self._stopping.set() # not necessary
        self._tasksets = tasksets
        self._optimization = optimization
        self._starting.set()
        
    def stop(self):
        self._stopping.set()

    def close(self):
        self._closing.set()

    def is_running(self):
        return self._running.is_set()
    
    def wait_stopping(self):
        """ Wait until taskset processing running."""
        self.logger.debug("waiting until distributor is stopped")
        while self._idle.wait(0.5):
            if not self.is_alive(): break

    def _ping_host(self):
        self.logger.debug("start pinging.")
        received_packages = re.compile(r"(\d) received")
        ping_out = os.popen("ping -q -c2 "+self._host,"r")
        while not self._closing.is_set():
            line = ping_out.readline()
            if not line: break
            n_received = re.findall(received_packages,line)
            if n_received:
                return int(n_received[0]) > 0
            return False

    def _live_request(self, distributor, taskset):
        # measure the time
        timestamp = time.clock()

        # requesting & handling callback
        live_request = distributor.live_request()
        delay = 5.0 # check status every five second
        if self.live_handler is not None:
            self.live_handler.__handle_request__(taskset, live_request)
            # but allow a higher resolution, too
            delay = min(delay, self.live_handler.__get_delay__())

        if not live_request.__is_running__():
            # processing of taskset is done
            self._processed_tasksets += 1
            self._running.clear()
            self._starting.set()
            if self.live_handler is not None:
                self.live_handler.__taskset_finish__(taskset)
            self.logger.debug("taskset is processed.")
        else:
            # do some waiting
            left = delay - (time.clock()-timestamp)
            if left < 0:
                self.logger.warning("Callback takes more time than espected. Live"
                                + " Request is delayed by {} ms.".format(-left))
            else:
                time.sleep(left/1000)


    def run(self):
        # ping host
        if self._ping:
            self._pinging.set()
            found = self._ping_host()
            self._pinging.clear()

            if not found:
                self.logger.debug("no host found. exiting.") 
                self._not_found.set()
                return
        self.logger.debug("host found. connecting...") 
        try:
            # establishing the connection is handled seperately.
            distributor = self._distributor_class(self._host, self._port)
            self.logger.info("connection established.")
        except socket.error as e:
            self.logger.critical(e)
            self._closing.set()
            return

        # fallback to idle mode
        self._idle.set()
        
        try:
            taskset = None 
            while not self._closing.is_set():
                # stopping (is always handled before new start requests)
                if self._stopping.is_set():
                    distributor.stop()
                    self._idle.set()
                    self._running.clear()
                    self._stopping.clear()
                    self.logger.debug("current taskset processing stopped.")
                    self.logger.debug("switch to idle mode.")
                    if self.live_handler is not None:
                        self.live_handler.__taskset_stop__(taskset)

                # try starting
                elif self._starting.is_set():
                    self._starting.clear()
                    try:
                        # pull taskset from queue and execute it.
                        taskset = self._tasksets.__next__()
                        distributor.start(taskset, self._optimization)
                        if self.live_handler is not None:
                            self.live_handler.__taskset_start__(taskset)
                        self._running.set()
                        self._idle.clear()
                        self.logger.debug("taskset processing started.")
                    except StopIteration:
                        # all tasksets are processed
                        self.logger.debug("all tasksets are processed.")
                        self.logger.debug("switch to idle mode.")
                # idle
                elif not self._running.is_set():
                    time.sleep(0.1)

                # as long as we are running, do live requests.
                elif self._running.is_set():
                    self._live_request(distributor, taskset)

                # How did we come here???
                else:
                    self.logger.critical("Distributor reached some unknown state.")
                
        except socket.error as e:
            self.logger.critical(e)
            # the current taskset is pushed back, so another distributor might
            # process it
            if taskset is not None:
                self._tasksets.put(taskset)

            # notify live handler about the stop.
            if self.live_handler is not None:
                        self.live_handler.__taskset_stop__(taskset)


        finally:
            distributor.close()
            self.logger.debug("distributor regularly closed.")
