import socket
import code
import struct
import re
import os
import subprocess
from collections import Iterable
import logging
import xmltodict
from abc import ABCMeta, abstractmethod

from taskgen.live import LiveResult
from taskgen.taskset import TaskSet
from taskgen.optimization import Optimization
from taskgen.distributor import AbstractDistributor


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
class SimpleDistributor(AbstractDistributor):

    def __init__(self, host, port):
        # it might happen, that creating a connection fails, so __init__
        # will throw an error. But that is ok.
        self._socket = socket.create_connection((host, port))
        self.logger = logging.getLogger("SimpleDistributor")

    def start(self, taskset, optimization):
        self._optimaze(optimization)
        self._clear()
        self._send_descs(taskset)
        self._send_bins(taskset)
        self._start()

    def stop(self):
        meta = struct.pack('I', MagicNumber.STOP)
        self.logger.debug('Stopping tasks on server.')
        self._socket.send(meta)
        self._stop()

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
            xml.decode('utf-8')[:-1]
            # convert xml to dictionary
        return xmltodict.parse(xml)
	
    def close(self):
        self._clear()
        self._socket.close()
        self.logger.debug('Close connection.')

    def optimize(self, optimization):
        if not isinstance(optimiziation, Optimiziation):
            raise TypeError("optimization must be of type Optimization") 

        self.logger.debug('Sending optimiziation goal.')
        # Read XML file and discard meta data.
        xml = optimiziation.dump()
        opt_ascii = xml.decode('ascii')

        # TODO make use of the new optimiziation class
        # Genode XML parser can't handle a lot of header things, so skip them.
        first_node = re.search('<\w+', opt_ascii)
        xml = xml[first_node.start():]
        meta = struct.pack('II', MagicNumber.OPTIMIZE, len(xml))

        self.conn.send(meta)
        self.conn.send(xml)

    def _clear(self):
        self.logger.debug('Resetting all tasks on server.')
        meta = struct.pack('I', MagicNumber.CLEAR)
        self._socket.send(meta)
        
    
    def _send_descs(self, taskset):
        if not isinstance(taskset, TaskSet):
            raise TypeError("taskset must be type TaskSet") 

        tasks = taskset.dump()
        tasks_ascii = tasks.decode('ascii')
        # Genode XML parser can't handle a lot of header things, so skip them.
        first_node = re.search('<\w+', tasks_ascii)
        tasks = tasks[first_node.start():]

        self.logger.debug("Sending taskset description.")
        meta = struct.pack('II', MagicNumber.SEND_DESCS, len(self.tasks))
        self._socket.send(meta)
        self._socket.send(self.tasks)
        
    def _send_bins(self, taskset):
        if not isinstance(taskset, TaskSet):
            raise TypeError("taskset must be type TaskSet") 

        tasks = taskset.dump()
        tasks_ascii = tasks.decode('ascii')
        # TODO need some fixing (we have the possibility to parse the dictionary structure)
        binaries = re.findall('<\s*pkg\s*>\s*(.+)\s*<\s*/pkg\s*>', tasks_ascii)
        binaries = list(set(binaries))

        self.logger.debug('Sending {} binar{}.'.format(len(binaries), 'y' if
                                                   len(binaries) == 1 else 'ies'))
        
        meta = struct.pack('II', MagicNumber.SEND_BINARIES, len(binaries))
        self._socket.send(meta)

        for name in self.binaries:
            # Wait for 'go' message.
            msg = int.from_bytes(self.conn.recv(4), 'little')
            if msg != GO_SEND:
                self.logger.critical('Invalid answer received, aborting: {}'.format(msg))
                break

            # TODO
            self.logger.debug('Sending {}.'.format(name))
            file = open(script_dir + name, 'rb').read()
            size = os.stat(script_dir + name).st_size
            meta = struct.pack('15scI', name.encode('ascii'), b'\0', size)
            self._socket.send(meta)
            self._socket.send(file)

    def _start(self):
        self.logger.debug('Starting tasks on server.')
        meta = struct.pack('I', MagicNumber.START)
        self._socket.send(meta)
        
