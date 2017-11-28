import os, re
from threading import Thread, Lock
from simple_distributor import StubDistributor, SimpleDistributor
from taskset import TaskSet

# debugging
import time


def dir_iterator(directory):
        for filename in os.listdir(directory):
                if filename.endswith(".xml"):
                        path = os.path.join(directory, filename)
                        yield open(path,'rb').read()

def file_iterator(path):
        return [open(path,'rb').read()]

def path_iterator(path):
    if os.path.isdir(path):
        return _dir_iterator(path)
    elif os.path.isfile(taskset):
        return _file_iterator(path)
    else:
        raise ValueError("Directory or file not found")

class threadsafe_iter:
    """Takes an iterator/generator and makes it thread-safe by
    serializing call to the `next` method of given iterator/generator.
    """
    def __init__(self, it):
        self.it = it
        self.lock = Lock()

    def __iter__(self):
        return self

    def __next__(self):
        with self.lock:
            return self.it.__next__()


class MultiDistributor:

    def __init__(self, hosts=None, port=None):
        self._hosts = hosts
        self._port = port
            
    def connect(self,hosts=None, port=None):
        if hosts is not None:
            self._hosts = hosts
        if port is not None:
            self._port = port
        
        if isinstance(self._hosts, list):
            pass
        elif isinstance(self._hosts, str):
            self._hosts = [self._hosts]
        else:
            raise TypeError("hosts must be [str] or str")
        
        self._dists = [SimpleThreadedDistributor(host, port) for host in
                       self._hosts]
        
    def start(self):
        for dist in self._dists:
            dist.read(self._tasksets) # handle over tasksets iterator 

        for dist in self._dists:
            dist.start() # start thread

    def read(self, taskset=None):       
        # a iterable object is stored.
        if isinstance(taskset, TaskSet):
            self._tasksets = taskset.produce()
        elif isinstance(taskset, Iterable):
            self._tasksets = taskset
        elif isinstance(taskset, str):
            self._tasksets = path_iterator(taskset)
        else:
            raise TypeError("taskset must be TaskSet, Iterable or str")

        # make the iterator thread safe
        self._tasksets = threadsafe_iter(self._tasksets)

    # TODO: stop, clear, live...

class SimpleThreadedDistributor(Thread, StubDistributor):
    # TODO: stop, live, profile...

    def __init__ (self, host, port):
        Thread.__init__(self)
        StubDistributor.__init__(self, host, port)

    def run(self):
        self.connect()
        for taskset in self._taskset:
            StubDistributor.read(self,taskset)
            StubDistributor.send_descs(self)
            StubDistributor.send_bins(self)
            StubDistributor.start(self)
            time.sleep(1)
            
    # TODO: WAITING, clear
    def start(self):
        Thread.start(self)

    def read(self, taskset):
        self._taskset = taskset # iterator
