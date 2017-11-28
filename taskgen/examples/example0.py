#!/usr/local/bin/python3

# go to taskgen's root directory
import sys
sys.path.append('../')

# import mixins
from mixins.gen_load_finite import GenLoadFiniteBlob
from mixins.priority import LowPriority, HighPriority
from mixins.tasks import PeriodicTask
from taskset import TaskSet

# debugging
from pprint import pprint as pp
import time


class SpecialTask(PeriodicTask, LowPriority, GenLoadFiniteBlob):
    pass

class SpecialTask2(PeriodicTask, HighPriority, GenLoadFiniteBlob):
    pass

ts = TaskSet()
ts.append( SpecialTask())
ts.append( SpecialTask2())


for t in ts.produce():
    print(t)

ts.export("./example0export")


