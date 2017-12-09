#!/usr/local/bin/python3
import logging
import sys
sys.path.append('../../')

from taskgen.tasksets.hey import HeyTaskSet

from taskgen.distributors.multi_distributor import MultiDistributor
from taskgen.distributors.log_distributor import LogDistributor
from taskgen.distributors.simple_distributor import SimpleDistributor

from pprint import pprint as pp


logging.basicConfig(level=logging.DEBUG)


ts = HeyTaskSet()

d = MultiDistributor(["172.25.1.5"], 3001)

d.start(ts)




