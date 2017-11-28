import subprocess
from ipaddress import ip_network
from platform import system as system_name # Returns the system/OS name
from os import system as system_call       # Execute a shell command
from multi_distributor import MultiDistributor

import os, re, threading


# CIDR format
# Distributor(["127.25.0.1"]) 
# Distributor(["127.25.0.0/5", "172.25.1.0/24"])
# Distributor("127.25.0.1")


class ScanDistributor(MultiDistributor):

    def __init__(self, hosts=None, port=None):
        super().__init__( hosts, port)

        
    def connect(self,hosts=None, port=None):
        # overwrite previews connection data
        if hosts is not None:
            self._hosts = hosts
        if port is not None:
            self._port = port

        # some checks
        if isinstance(self._hosts, list):
            pass
        elif isinstance(self._hosts, str):
            self._hosts = [hosts]
        else:
            raise TypeError("hosts must be [str] or str")

        # calcuate all ip addresses
        hosts_all = []
        for host in self._hosts:
            for host_single in ip_network(host).hosts():
                hosts_all.append(host_single)

        # start threads for pinging
        check_results = []
        for host in hosts_all:
            current = self.ip_check(host)
            check_results.append(current)
            current.start()

        # wait until thread terminates
        hosts_found = []
        for el in check_results:
            el.join()
            if el.status() > 0:
                hosts_found.append(el.ip)

        # do the actual connection 
        super().connect(hosts_found, port)

        
    # Thread subclass, which does the pinging
    class ip_check(threading.Thread):
        received_packages = re.compile(r"(\d) received")
        def __init__ (self,ip):
            threading.Thread.__init__(self)
            self.ip = ip
            self.__successful_pings = -1                        
                        
        def run(self):
            print("ping: {} start".format(str(self.ip)))
            ping_out = os.popen("ping -q -c2 "+str(self.ip),"r")
            while True:
                line = ping_out.readline()
                if not line: break
                n_received = re.findall(self.received_packages,line)
                if n_received:
                    self.__successful_pings = int(n_received[0])
                    print("ping: {} received: {}".format(str(self.ip), self.status()))
        def status(self):
            return self.__successful_pings
                    



