#!/usr/local/bin/python3

# go to taskgen's root directory
import sys
sys.path.append('../')

from tasksets.tasks import PeriodicTask, AperiodicTask, Task
from tasksets.taskset import TaskSet
from tasksets.mixins.priority import LowPriority
from tasksets.mixins.gen_load_finite import GenLoadFiniteBlob


from pprint import pprint as pp

class SpecialTask(LowPriority, AperiodicTask):
    pass



