#!/usr/local/bin/python3

# go to taskgen's root directory
import sys
sys.path.append('../')

# import mixins
from mixins.gen_load_finite import GenLoadFiniteBlob
from mixins.priority import LowPriority, HighPriority
from mixins.tasks import PeriodicTask
from taskset import TaskSet
from simple_distributor import SimpleDistributor

from taskset import TaskSet
from simple_distributor import SimpleDistributor


import mixins

# mix new taskset with Mixins
class MixedTask(PeriodicTask, LowPriority, GenLoadFiniteBlob):
    pass

task = MixedTask()

# oder
task = PeriodicTask()
task["priority"] = range(0, 20)
# ...



mixed = MixedTask()

# generate all tasksets
tasksets = mixed.generate()

# save single taskset
tasksets[0].save("./taskset.xml")

# save all tasksets
TaskSet.save(tasksets, "./tasksets/")

taskset = TaskSet()
taskset.read("./taskset.xml")

# loop over all tasks
for task in taskset:
    print task


sd = SimpleDistributor().connect()




