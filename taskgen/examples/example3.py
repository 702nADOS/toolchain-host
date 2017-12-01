#!/usr/local/bin/python3

# go to taskgen's root directory
import sys
sys.path.append('../')

from scan_distributor import ScanDistributor
from mixins.gen_load_finite import GenLoadFiniteBlob
from mixins.priority import LowPriority, HighPriority
from mixins.tasks import PeriodicTask
from taskset import TaskSet

class SpecialTask(PeriodicTask, LowPriority, GenLoadFiniteBlob):
    pass

tasksets = mixed.generate()

md = ScanDistributor(["131.159.197.0/24"], 1024)
md.tasksets += tasksets
md.start()




