import socket
import code
import struct
import re
import os
import sys
import subprocess
from collections import Iterable
import logging
import xmltodict
from abc import ABCMeta, abstractmethod
from taskgen.distributor import AbstractSession
from taskgen.taskset import TaskSet
from taskgen.optimization import Optimization
import taskgen
import time

# capsulation avoids attribute pollution
class MagicNumber:
    # Packet contains task descriptions as XML. uint32_t after tag indicates size in
    # bytes.
    SEND_DESCS = 0xDE5

    # Clear and stop all tasks currently managed on the server.
    CLEAR = 0xDE6

    # Multiple binaries are to be sent. uint32_t after tag indicates number of
    # binaries. Each binary packet contains another leading uint32_t indicating
    # binary size.
    SEND_BINARIES = 0xDE5F11E
    
    # Binary received, send next one.
    GO_SEND = 0x90

    # Start queued tasks.
    START = 0x514DE5

    # Stop all tasks.
    STOP = 0x514DE6

    # Request profiling info as xml.
    GET_PROFILE = 0x159D1
    
    # Request live info as xml
    GET_LIVE = 0x159D2
    
    #Initiate task scheduling optimization.
    OPTIMIZE = 0x6F7074


    
# This class is a pretty simple implementation for the communication with a
# genode::Taskloader instance. There are no error handling mechanism and all
# errors are passed on to the caller. Furthmore, the communication is not
# asyncron, which means that every call is blocking. Look at the
# MultiDistributor and ScanDistributor for a more extended version.
class GenodeSession(AbstractSession):
    
    def __init__(self, host, port):
        self._socket = socket.create_connection((host, port))
        self.logger = logging.getLogger("GenodeSession")
        self.logger.debug("Connection establishment")
        self._socket.settimeout(10.0) # wait 10 seconds for responses...
        
    def start(self, taskset, optimization=None):
        self._clear()
        # TODO clear recv buffer
        
        if optimization is not None:
            self._optimaze(optimization)

        self._send_descs(taskset)
        self._send_bins(taskset)
        self._start()

    def stop(self):
        self._stop()

    def close(self):
#        self._clear()  what if the connection is dead...
        self._close()
        

    def optimize(self, optimization):
        if not isinstance(optimiziation, Optimiziation):
            raise TypeError("optimization must be of type Optimization") 

        self.logger.debug('Send optimiziaton goal.')
        # Read XML file and discard meta data.
        xml = optimiziation.dump()
        opt_ascii = xml.decode('ascii')

        # TODO make use of the new optimiziation class
        # Genode XML parser can't handle a lot of header things, so skip them.
        first_node = re.search('<\w+', opt_ascii)
        xml = xml[first_node.start():]
        meta = struct.pack('II', MagicNumber.OPTIMIZE, len(xml))

        self._socket.send(meta)
        self._socket.send(xml)

    def _close(self):
        self._socket.close()
        self.logger.debug('Close connection.')
        
    def _stop(self):
        meta = struct.pack('I', MagicNumber.STOP)
        self.logger.debug('Stop tasks on server.')
        self._socket.send(meta)
        
    def _clear(self):
        self.logger.debug('Clear tasks on server.')
        meta = struct.pack('I', MagicNumber.CLEAR)
        self._socket.send(meta)
            
    def _send_descs(self, taskset):
        if not isinstance(taskset, TaskSet):
            raise TypeError("taskset must be type TaskSet") 

        description = taskset.description()
        self.logger.debug("Sending taskset description.")
        meta = struct.pack('II', MagicNumber.SEND_DESCS, len(description))
        self._socket.send(meta)
        self._socket.send(description.encode("ascii"))

    def event(self):
        # buffered reader
        # find xml file, read
        # parse to dict
        # return
        time.sleep(4)
        return { 'running' : True }

        """
        # receive xml
        size = int.from_bytes(self._socket.recv(4), 'little')
        xml = b''
        while len(xml) < size:
            xml += self._socket.recv(size)

        return xml.decode('utf-8')[:-1]
        """

        
    def _send_bins(self, taskset):
        if not isinstance(taskset, TaskSet):
            raise TypeError("taskset must be type TaskSet") 

        binaries = taskset.binaries()
        self.logger.debug('Sending {} binary file(s).'.format(len(binaries)))
        
        meta = struct.pack('II', MagicNumber.SEND_BINARIES, len(binaries))
        self._socket.send(meta)

        # get the path to the bin folder
        bin_path = "/home/fischejo/university/informatik/in2261-bachelor/bsc-taskgen/toolchain-host/taskgen/bin/"
        
        for name in binaries:
            # Wait for 'go' message.
            msg = int.from_bytes(self._socket.recv(4), 'little')
            if msg != MagicNumber.GO_SEND:
                self.logger.critical('Invalid answer received, aborting: {}'.format(msg))
                break

            self.logger.debug('Sending {}.'.format(name))
            file = open(bin_path + name, 'rb').read()
            size = os.stat(bin_path + name).st_size
            meta = struct.pack('15scI', name.encode('ascii'), b'\0', size)
            self._socket.send(meta)
            self._socket.send(file)

    def _start(self):
        self.logger.debug('Starting tasks on server.')
        meta = struct.pack('I', MagicNumber.START)
        self._socket.send(meta)
        


class PingSession(GenodeSession):
        
    # overwrite the availiblity check and replace it with a ping.
    def is_available(host):
        received_packages = re.compile(r"(\d) received")
        ping_out = os.popen("ping -q -W {} -c2 {}".format(4, host),"r")
        while True:
            line = ping_out.readline()
            if not line:
                break
            n_received = re.findall(received_packages,line)
            if n_received:
                return int(n_received[0]) > 0


