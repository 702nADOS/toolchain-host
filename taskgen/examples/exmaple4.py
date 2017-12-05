#!/usr/local/bin/python3

# go to taskgen's root directory
import sys
sys.path.append('../')

from tasksets.mixins.tasks2 import PeriodicTask, SporadicTask
from tasksets.mixins.priority import LowPriority
from tasksets.mixins.gen_load_finite import GenLoadFiniteBlob
from tasksets.taskset import TaskSet
from tasksets.example1 import Example1TaskSet

from pprint import pprint as pp




t = PeriodicTask()
print(t)
