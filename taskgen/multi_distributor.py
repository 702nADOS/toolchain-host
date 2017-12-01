import os, re
import threading
import time
from simple_distributor import SimpleDistributor, AbstractDistributor
from taskset import TaskSet
from collections.abc import Mapping
import logging
from live import AbstractLiveHandler, LiveResult
import subprocess
from ipaddress import ip_network
from itertools import chain

# die eierlegende Wohlmilchsau
class MultiDistributor(Mapping):
    def __init__(self, hosts, port, ping=True, distributor_class=SimpleDistributor):
        self._live_handler = None

        if not isinstance(hosts, str):
            hosts = [hosts]
        elif isinstance(hosts, list) and all(isinstance(h, str) for h in hosts):
            pass
        else:
            raise TypeError("hosts must be [str] or str.")
        
        if not isinstance(port, int):
            raise TypeError("port must be int")

        if not isinstance(distributor_class, AbstractDistributor):
            raise TypeError("distributor_class must be of type AbstractDistributor")

        # unpack all ip addresses from range definitions
        hosts = chain.from_iterable([ip_network(host).hosts() for host in hosts])
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
        if not isinstance(live_handler, AbstractLiveHandler):
            raise TypeError("live_handler must have BaseClass AbstractLiveHandler")
        self._live_handler = live_handler

    def start(self, tasksets, optimization=None):
        if not isinstance(optimiziation, Optimiziation):
            raise TypeError("optimization must be of type Optimization")

        # wrap tasksets into an threadsafe iterator
        tasksets = _threadseafe_iter(tasksets)
        # to prevent later changes at the opimization structure, do a full copy
        # of the object
        optimization = copy.deepcopy(optimization)

        # lets inform the single distributors about their new work
        for distributor in self._distributors.values():
            distributor.start(tasksets, optimization)

    def stop(self):
        for distributor in self._distributors.values()
            distributor.stop()
        
    def close(self):
        for distributor in self._distributors.values()
            distributor.close()        
            
    def __getitem__(self, ii):
        return self.build_state(_distributors[ii])

    def __iter__(self):
        return iter(map(lambda d : self._build_state(self_.distributors)))

    def __len__(self):
        return len(self._optimization)

    def _build_state(self, distributor):
        # is this performant?
        return {
            'starting': distributor.is_starting(),
            'running': distributor.is_running(),
            'stopping': distributor.is_stopping(),
            'closing': distributor.is_closing(),
            'closed': distributor.is_alive(),
            'processed_tasksets': distributor.processed_tasksets()
        }

            
class _threadsafe_iter:
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


class _ThreadedWrapperDistributor(threading.Thread):
    # DO NOT USE THIS CLASS. It is threaded and some attributes are not
    # thread-safe! This is a internal class for MultiDistributor
    
    def __init__ (self, host, port, ping=True, distributor_class=AbstractDistributor):
        Thread.__init__(self)
        # all commands are stored in this queue and processed by the thread. No
        # method of SimpleThreadedDistributor will be blocking. The Queue is
        # infinite.
        self._tasksets = None
        self._optimiziation = None
        self.live_handler = None
        self._distributor_class = distributor_class
        self._ping = ping
        self._found_host = False
        
        # start the thread immediately
        Thread.start()

        # represents the internal state (_running and _idle are exclusive)
        self._running = threading.Event()
        self._idle = threading.Event() # necessary for blocking event
        
        # triggers from other threads
        self._stopping = threading.Event()
        self._starting = threading.Event()
        self._closing = treading.Event()

        self._processed_tasksets = 0

    def found_host(self):
        return _self._found_host
    
    def is_closing(self):
        return self._closing.is_set()
    
    def start(self, wait=True):
        self._starting.set()
        if wait: self._running.wait()
        
    def stop(self, wait=True):
        self._stopping.set()
        if wait: self._idle.wait()

    def close(self, wait=True):
        self._closing.set()
        if wait: Thread.join()
        
        
    def is_starting(self):
        return self._starting.is_set()

    def is_stopping(self):
        return self._stopping.is_set()

    def is_running(self):
        # same as (not self._idle.is_set())
        return self._running.is_set()

    def processed_tasksets(self):
        return self._processed_tasksets

    def _ping(self):
        logging.debug("start ping: {}".format(self._ip))

        ping_out = os.popen("ping -q -c2 "+str(self.ip),"r")
        while not self.is_closing():
            line = ping_out.readline()
            if not line: break
            n_received = re.findall(self.received_packages,line)
            if n_received:
                return int(n_received[0]) > 0
            return false
                
    def _live_request(distributor, taskset):
        # measure the time
        time = time.clock()

        # requesting & handling callback
        live_request = distributor.live_request()            
        delay = 5.0 # check status every five second
        if self.live_handler is not None:
            self.live_handler.__handle__(taskset, live_request)
            # but allow a higher resolution, too
            delay = min(delay, self.live_handler.__get_delay__())

        if not live_request.is_running():
            # processing of taskset is done
            self._processed_tasksets += 1
            self._running.clear()
        else:
            # do some waiting
            left = delay - (time.clock()-time)
            if left < 0:
                logging.warning("Callback takes more time than espected. Live
                Request is delayed by {} ms.".format(-left))
            else:
                time.sleep(left/1000)
                

    def _clear_start(self, distributor):
        # send the optimization
        if self._optimization is not None:
            distributor.optimize(self._optimization)

        # clear old taskset
        distributor.clear()
        
        # pull new taskset from queue and send it
        taskset = self._tasksets.get()                    
        distributor.send_descs(taskset)
        distributor.send_bins(taskset)
                
        # start executing taskset
        distributor.start()
        return taskset

    def run(self):
        # ping host
        if self._ping:
            self._found_host = self._ping()

        # found no host
        if not self._found_host:
            return

        try:
            # try to connect
            distributor = self._distributor_class(self._host, self._port)
            taskset = None 

            while not self.is_closing():

                # stopping is always handled before new start requests
                if self.is_stopping():
                    distributor.stop()
                    self._idle.set()
                    self._running.clear()
                    self._stopping.clear()
                    
                # there is the option to send another start signal, while
                # running. That is ok, because a clear/stop request is always
                # send before each start request.
                elif self.is_starting():
                    self._clear_start(distributor)
                    self._idle.clear()
                    self._running.set()
                    taskset = self._starting.clear()
                # idle
                elif not self.is_running():
                    time.sleep(0.1)

                # as long as we are running, do live requests.
                elif self.is_running():
                    self._live_request(distributor, taskset)

                # How did we come here???
                else:
                    logging.critical("Reached some unknown state")
                
            # clear and finally close
            distributor.clear()
        except socket.error as e:
            logging.critical(e)
        finally:
            distributor.close()
            self._closed = True
