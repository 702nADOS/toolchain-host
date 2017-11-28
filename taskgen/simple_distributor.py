import socket
import code
import struct
import magicnumbers
import re
import subprocess
from collections import Iterable
from taskset import TaskSet
import os

COLORS = ["\033[1;31m","\033[1;34m","\033[1;36m","\033[0;32m"]
def color():
    color.counter += 1
    return  COLORS[color.counter % len(COLORS)]
color.counter = 0

class StubDistributor:
    
    def printc(self, s):
        print(self._color + s + "\033[0;0m")
        
    def __init__(self, host, port):
        self._host = host
        self._port = port

        # color fun
        self._color = color()
        
        self.printc("StubDistributor({},{})".format(self._host, self._port))

    def connect(self):
        self.printc("StubDistributor({},{}).connect()".format(self._host, self._port))

    def read_file(self, file):
        if isinstance(path, str) and os.path.isfile(path):
            self.printc("StubDistributor({},{}).read_file()".format(self._host,
                                                                self._port, path))
        else:
            raise ValueError("file not found")
        
    def read(self, dump):
        if isinstance(dump, str):
            self.printc("StubDistributor({},{}).read()".format(self._host,
                                                             self._port))
        self._dump = dump;
    def send_descs(self):
        self.printc("StubDistributor({},{})._send_descs()".format(self._host,
                                                            self._port))
        
    def send_bins(self):
        self.printc("StubDistributor({},{})._send_bins()".format(self._host,
                                                           self._port))
        
    def start(self):
        self.printc("StubDistributor({},{}).start()".format(self._host,
                                                      self._port))
        self.printc(self._dump)

    def stop(self):
        self.printc("StubDistributor({},{}).stop()".format(self._host,
                                                     self._port))

    def clear(self):
        self.printc("StubDistributor({},{}).clear()".format(self._host,
                                                      self._port))

    def profile(self, log_file='log.xml'):
        self.printc("StubDistributor({},{}).profile(...)".format(self._host,
                                                           self._port))

    def live(self, log_file='log.xml'):
        self.printc("StubDistributor({},{}).live(...)".format(self._host,
                                                        self._port))

    def optimize(self, opt_file='opt.xml'):
        self.printc("StubDistributor({},{}).optimize(...)".format(self._host,
                                                            self._port))
	
    def close(self):
        self.printc("StubDistributor({},{}).close()".format(self._host,
                                                      self._port))


    
    

class SimpleDistributor():
    def __init__(self, host='192.168.217.20', port=3001):
        self._host = host
        self._port = port

    def connect(self):
        self.conn = socket.create_connection((self._host, self._port))

    def read_file(self, file):
        if isinstance(path, str) and os.path.isfile(path):
            # Read XML file and discard meta data.
            self.read(open(path, 'rb').read())
        else:
            raise ValueError("file not found")
        
    def read(self, dump):
        self.tasks = dump

        # do the old magic
        tasks_ascii = self.tasks.decode('ascii')

        self.binaries = re.findall('<\s*pkg\s*>\s*(.+)\s*<\s*/pkg\s*>', tasks_ascii)
        self.binaries = list(set(self.binaries))

        # Genode XML parser can't handle a lot of header things, so skip them.
        first_node = re.search('<\w+', tasks_ascii)
        self.tasks = self.tasks[first_node.start():]
        
    def _send_descs(self):
        """Send task descriptions to the dom0 server."""
        meta = struct.pack('II', magicnumbers.SEND_DESCS, len(self.tasks))
        print('Sending tasks description.')
        self.conn.send(meta)
        self.conn.send(self.tasks)
        
    def _send_bins(self):
        """Send binary files to the dom0 server."""
        meta = struct.pack('II', magicnumbers.SEND_BINARIES, len(self.binaries))
        print('Sending {} binar{}.'.format(len(self.binaries), 'y' if
                                           len(self.binaries) == 1 else 'ies'))
        self.conn.send(meta)

        for name in self.binaries:
            # Wait for 'go' message.
            msg = int.from_bytes(self.conn.recv(4), 'little')
            if msg != magicnumbers.GO_SEND:
                print('Invalid answer received, aborting: {}'.format(msg))
                break
            
            print('Sending {}.'.format(name))
            file = open(script_dir + name, 'rb').read()
            size = os.stat(script_dir + name).st_size
            meta = struct.pack('15scI', name.encode('ascii'), b'\0', size)
            self.conn.send(meta)
            self.conn.send(file)
            
    def start(self):
        """Send message to start the tasks on the server."""
        print('Starting tasks on server.')
        meta = struct.pack('I', magicnumbers.START)
        self.conn.send(meta)
        
    def stop(self):
        """Send message to kill all tasks."""
        print('Stopping tasks on server.')
        meta = struct.pack('I', magicnumbers.STOP)
        self.conn.send(meta)
        
    def clear(self):
        """Send command to stop all tasks and clear the current task set."""
        print('Resetting all tasks on server.')
        meta = struct.pack('I', magicnumbers.CLEAR)
        self.conn.send(meta)
        
    def profile(self, log_file='log.xml'):
        """Get profiling information about all running tasks."""
        print('Requesting profile data.')
        meta = struct.pack('I', magicnumbers.GET_PROFILE)
        self.conn.send(meta)
        
        size = int.from_bytes(self.conn.recv(4), 'little')
        xml = b''
        while len(xml) < size:
            xml += self.conn.recv(size)
            file = open(log_file, 'w')
            file.write(xml.decode('utf-8')[:-1])
            print('Profiling data of size {} saved to {}'.format(size, log_file))

    def live(self, log_file='log.xml'):
        """Get profiling information about all running tasks."""
        meta = struct.pack('I', magicnumbers.GET_LIVE)
        self.conn.send(meta)
        
        size = int.from_bytes(self.conn.recv(4), 'little')
        xml = b''
        while len(xml) < size:
            xml += self.conn.recv(size)
            file = open(log_file, 'w')
            file.write(xml.decode('utf-8')[:-1])
            #subprocess.call('clear', shell=True)
            #print(xml.decode('utf-8')[:-1])
            print('Live data of size {} saved to {}'.format(size, log_file))

    def optimize(self, opt_file='opt.xml'):
        """Read XML file to get optimization goal."""
        # Read XML file and discard meta data.
        self.opt = open(opt_file, 'rb').read()
        opt_ascii = self.opt.decode('ascii')
        
        # Genode XML parser can't handle a lot of header things, so skip them.
        first_node = re.search('<\w+', opt_ascii)
        self.opt = self.opt[first_node.start():]
	
	
        """Send optimize goal to the dom0 server."""
        meta = struct.pack('II', magicnumbers.OPTIMIZE, len(self.opt))
        print('Sending optimization goal.')
        self.conn.send(meta)
        self.conn.send(self.opt)
	
    def close(self):
        """Close connection."""
        self.conn.close();
