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




class TaskA(PeriodicTask, GenLoadFiniteBlob):    pass

class TaskB(SporadicTask, LowPriority, GenLoadFiniteBlob):    pass 

class ExampleTaskSet(TaskSet):
    def __init__(self):
        super().__init__()
        # my custom TaskSet
        self.append(TaskA())
        
ts_1 = Example1TaskSet()


ts_a = ExampleTaskSet()



for a in ts_1.variants():
g    print(a.asxml())


