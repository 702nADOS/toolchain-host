#!/usr/local/bin/python3
import logging
import sys
sys.path.append('../../')
import time
from taskgen.tasksets.hey import HeyTaskSet
from taskgen.distributor import Distributor

from pprint import pprint as pp


logging.basicConfig(level=logging.DEBUG)


ts = HeyTaskSet()

d = Distributor(["172.25.1.5"], 3001)

d.start(ts)


print("proof: done")

d.close()

print("proof: closed")
