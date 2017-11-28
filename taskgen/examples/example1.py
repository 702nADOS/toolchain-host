#!/usr/local/bin/python3

# go to taskgen's root directory
import sys
sys.path.append('../')

from simple_distributor import SimpleDistributor

sd = SimpleDistributor("192.168.1.1", 1024)
sd.connect()
