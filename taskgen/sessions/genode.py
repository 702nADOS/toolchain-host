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
        
    def live_request(self):
        self.logger.debug('Requesting live data.')
        # send command
        meta = struct.pack('I', MagicNumber.GET_LIVE)
        self._socket.send(meta)
        # receive xml
        size = int.from_bytes(self._socket.recv(4), 'little')
        xml = b''
        while len(xml) < size:
            xml += self._socket.recv(size)

        return xml.decode('utf-8')[:-1]

    def optimize(self, optimization):
        if not isinstance(optimiziation, Optimiziation):
            raise TypeError("optimization must be of type Optimization") 

        self.logger.debug('Send optimiziation goal.')
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

        tasks = taskset.asxml()
        tasks_ascii = tasks #.encode('ascii')
        # Genode XML parser can't handle a lot of header things, so skip them.
        first_node = re.search('<\w+', tasks_ascii)
        tasks = tasks[first_node.start():]

        self.logger.debug("Sending taskset description.")
        meta = struct.pack('II', MagicNumber.SEND_DESCS, len(tasks))
        self._socket.send(meta)
        self._socket.send(tasks.encode("ascii"))
        
    def _send_bins(self, taskset):
        if not isinstance(taskset, TaskSet):
            raise TypeError("taskset must be type TaskSet") 

        tasks = taskset.asxml()
        tasks_ascii = tasks
        # TODO need some fixing (we have the possibility to parse the dictionary structure)
        binaries = re.findall('<\s*pkg\s*>\s*(.+)\s*<\s*/pkg\s*>', tasks_ascii)
        binaries = list(set(binaries))

        self.logger.debug('Sending {} binar{}.'.format(len(binaries), 'y' if
                                                   len(binaries) == 1 else 'ies'))
        
        meta = struct.pack('II', MagicNumber.SEND_BINARIES, len(binaries))
        self._socket.send(meta)

        # get the path to the bin folder
        bin_path = taskgen.__path__[0] + "/bin/"
        
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
        
