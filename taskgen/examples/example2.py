#!/usr/local/bin/python3

# go to taskgen's root directory
import sys
sys.path.append('../')

from multi_distributor import MultiDistributor
from mixins.gen_load_finite import GenLoadFiniteBlob
from mixins.priority import LowPriority, HighPriority
from mixins.tasks import PeriodicTask
from taskset import TaskSet

class SpecialTask(PeriodicTask, LowPriority, GenLoadFiniteBlob):
    pass

ts = TaskSet()
ts.append( SpecialTask())

md = MultiDistributor(["192.168.1.0","192.168.1.0","192.168.1.0","192.168.1.0", "102.157.2.1"], 1024)
md.connect()
md.read(ts)
md.start()




