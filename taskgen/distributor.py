from abc import ABCMeta, abstractmethod
import threading
import time
import logging
import subprocess
import copy
import socket
from queue import Empty, Queue, Full
from collections.abc import Mapping
from ipaddress import ip_network, ip_address
from itertools import chain
from math import ceil

from taskgen.optimization import Optimization
from taskgen.taskset import TaskSet
from taskgen.event import AbstractEventHandler, taskset_is_processing


# we need some conventions, to ensure that the Distributor is working
class AbstractSession(metaclass=ABCMeta):

    @staticmethod
    def is_available(host):
        return True
    
    @abstractmethod
    def __init__(self, host, port):
        pass

    @abstractmethod
    def start(self, optimization, taskset):
        pass
    
    @abstractmethod
    def start(self, optimization, taskset):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def event(self):
        pass

    @abstractmethod
    def close(self):
        pass

# GenodeSession depends on AbstractSession...
from taskgen.sessions.genode import PingSession

class Distributor:
    
    def __init__(self,
                 destinations,
                 port=3001,
                 session_class=PingSession,
                 starter_threads = 15):

        if not isinstance(port, int):
            raise TypeError("port must be int")

        if not issubclass(session_class, AbstractSession):
            raise TypeError("session_class must be a class with subtype AbstractSession")

        self._sessions = []
        self._starter = []
        self._port = port
        self._session_class = session_class
        self.logger = logging.getLogger('Distributor')
        self._close_event = threading.Event()
        self._pool = Queue()
        self._event_handler = None
        self._run = False
        self._tasksets = None
        self._optimization = None
        
        # build pool of IP destination addresses
        if isinstance(destinations, str):
            self._append_pool(destinations)
        elif isinstance(destinations, list):
            for destination in destinations:
                self._append_pool(destination)
        else:
            raise TypeError("destinations must be [str] or str.")

        # initialize pinging and connecting of destinations
        for c in range(0, starter_threads):
            starter = threading.Thread(target=Distributor._starter, args=(self,))
            starter.start()
            self._starter.append(starter)        

            
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

            
    @staticmethod
    def _starter(self):
        while not self._close_event.is_set():
            try:
                host = self._pool.get(True, 2)
                if self._session_class.is_available(host):
                    self.logger.info("Found {}".format(host))
                    # initalize session
                    session = _WrapperSession(host,
                                              self._port,
                                              self._close_event,
                                              self._session_class,
                                              self._pool,
                                              self._sessions)
                    session.event_handler = self.event_handler
                    # start session
                    if self._run:
                        session.start(self._tasksets, self._optimization)
                    session.thread_start()
                    self._sessions.append(session)
                else:
                    self._pool.put(host)
            except Empty:
                pass

    @property
    def event_handler(self):
        return self._event_handler
            
    @event_handler.setter
    def event_handler(self, event_handler):
        if event_handler is not None:
            if not isinstance(event_handler, AbstractEventHandler):
                raise TypeError("event_handler must be of type AbstractEventHandler")
        self._event_handler = event_handler
        for session in self._sessions:
            session.event_handler = event_handler

            
    def start(self, taskset, optimization=None, wait=True):

        if taskset is None or not isinstance(taskset, TaskSet):
            raise TypeError("taskset must be TaskSet.")

        if optimization is not None:
            if not isinstance(optimization, Optimization):
                raise TypeError("optimization must be of type Optimization")

        # wrap tasksets into an threadsafe iterator
        self._tasksets = _TaskSetQueue(taskset.variants())
        self._optimization = optimization
        self._run = True
        for session in self._sessions:
            session.start(self._tasksets, optimization)
        if wait: self.wait_finished()

    def stop(self, wait=True):
        self.logger.info("Stop processing taskset")
        self._run = False
        for session in self._sessions:
            session.stop()
        if wait: self.wait_stopped()
        
    def close(self, wait=True):
        self._close_event.set()
        self.logger.info("Closing connections...")
        if wait: self.wait_closed()

    def wait_closed(self):
        self.logger.info("Waiting until ping threads are stopped")
        for starter in self._starter:
            starter.join()

        # TODO: when closing, it might happen that a starter thread still opens a connection.
        # the log message then might be disturbing.
        self.logger.info("Waiting until sessions are closed")
        for session in self._sessions:
            session.join()
        
    def wait_stopped(self):
        self.logger.info("Waiting until session processings are stopped")
        for session in self._sessions:
            session.wait_stopped()

    def wait_finished(self):
        while not self._close_event.is_set():
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
        self.in_progress = []
        self.processed = 0
        self.logger = logging.getLogger("Distributor")
        
    def get(self):
        # return a regular taskset
        with self.lock:
            taskset = None
            if not self.queue.empty():
                try:
                    taskset = self.queue.get_nowait()
                except Queue.Empty:
                    # ups, another distributor just stole our taskset
                    pass

            # take a new one from the iterator
            if taskset is None:
                taskset = self.it.__next__()

            # keep track of current processed tasksets
            self.in_progress.append(taskset)
            return taskset
            
    def empty(self):
        with self.lock:
            # in progress?
            if len(self.in_progress) > 0:
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

    def done(self, taskset):
        with self.lock:
            self.in_progress.remove(taskset)
            self.processed += 1
            self.logger.info("{} taskset variant(s) processed".format(self.processed))
        
    def put(self, taskset):
        with self.lock:
            try:
                self.in_progress.remove(taskset)
                self.queue.put_nowait(taskset)
            except Full:
                # We don't care about the missed taskset. Actually, there is a bigger
                # problem:
                self.logger.critical("The Push-Back Queue of tasksets is full. This is a"
                    + "indicator, that the underlying session is buggy"
                    + " and is always canceling currently processed tasksets.")

            

class _WrapperSession(threading.Thread):
    
    def __init__ (self, host, port, close, session_class, pool, sessions):
        
        super().__init__()
        self._host = host
        self._port = port
        self._pool = pool
        self._sessions = sessions
        self._tasksets = None
        self.event_handler = None
        self._close = close
        self._session_class = session_class
        self._logger = logging.getLogger("Distributor({})".format(host))

        self._taskset = None
        self._running = False
        self._restart_lock = threading.Lock()
        self._run = False

    def thread_start(self):
        threading.Thread.start(self)

    def wait_stopped(self):
        while self._running and self._run and not self._close.is_set():
            time.sleep(0.5)

    def start(self, tasksets, optimization):
        with self._restart_lock:
            self._tasksets = tasksets
            self._optimization = optimization
            self._restart = True
            self._run = True

    def stop(self):
        self._run = False

            
    def _internal_start(self, session):
        try:
            with self._restart_lock:
                tasksets = self._tasksets
                optimization = self._optimization
                
            self._taskset = tasksets.get()
            session.start(self._taskset, optimization)
            if self.event_handler is not None:
                self.event_handler.__taskset_start__(self._taskset)
                
            self._logger.debug("Taskset variant processing started.")
            self._restart = False
            self._running = True
        except StopIteration:
            # all tasksets are processed
            self._logger.debug("All taskset variants are processed")
            self._running = False
            self._restart = False
            self._taskset = None


    def _internal_stop(self, session):
        session.stop()
        if self._taskset is not None :
            if self.event_handler is not None:
                self.event_handler.__taskset_stop__(self._taskset)
            self._tasksets.put(self._taskset)
            self._taskset = None
        self._running = False


        
    def _internal_event_handling(self, session):
        # requesting & handling callback
        event = session.event()

        if self.event_handler is not None:
            self.event_handler.__taskset_event__(self._taskset, event)
        target_running = taskset_is_processing(event)

        if not target_running:
            if self.event_handler is not None:
                self.event_handler.__taskset_finish__(self._taskset)
            self._tasksets.done(self._taskset)  # notify about the finished taskset
            self._logger.debug("Taskset variant is successfully processed")
            
        return target_running

    
    def run(self):
        # try to connect
        try:
            session = self._session_class(self._host, self._port)
            self._logger.info("Connection established.")
        except socket.error as e:
            self._logger.critical(e)
            self._pool.put(self._host)
            return 

        try:
            while not self._close.is_set():
                # stopping
                if not self._run and self._running:
                    self._internal_stop(session, taskset)
                # restart or still running
                if self._restart or self._running:
                    # try to start next taskset
                    self._internal_start(session)

                    # live requests
                    while (not self._close.is_set() and not self._restart and
                           self._run and self._running):
                        if not self._internal_event_handling(session):
                            break
                # idle
                elif not self._running:
                    time.sleep(0.1)
                else:
                    self._logger.critical("Reached some unknown state")
                    time.sleep(0.1)

            self._internal_stop(session)
        except socket.error as e:
            self._logger.critical(e)
            
            if self._taskset is not None:
                self._tasksets.put(self._taskset)
                self._logger.debug("Taskset variant is pushed back to queue due to" +
                                   " a critical error")
                # notify live handler about the stop.
                if self.event_handler is not None:
                    self.event_handler.__taskset_stop__(self._taskset)

            # push host back in pool (only, if there was an error). A closing
            # event does not trigger the push back to the host pool.
            self._sessions.remove(self)
            self._pool.put(self._host)

            # if this was the last processing session, you will get notified
            # about missing sessions.
            if not self._tasksets.empty() and len(self._sessions) == 0:
                self._logger.warning("No session is left for processing further" +
                                      " taskset variants. Waiting for new sessions.")
        finally:
            session.close()

