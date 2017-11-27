#!/usr/local/bin/python3

# go to taskgen's root directory
import sys
sys.path.append('../')

# import mixins
from mixins.gen_load_finite import GenLoadFiniteBlob
from mixins.priority import LowPriority, HighPriority
from mixins.tasks import PeriodicTask

from pprint import pprint as pp
import time


class SpecialTask(PeriodicTask, LowPriority, GenLoadFiniteBlob):
    pass



a = SpecialTask()

start = time.time()
a.produce2()
end = time.time()
print(end - start)
