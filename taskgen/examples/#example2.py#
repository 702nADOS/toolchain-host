#!/usr/local/bin/python3

# go to taskgen's root directory
import sys
sys.path.append('../')

from multi_distributor import MultiDistributor
from simple_distributor import SimpleDistributor, StubDistributor
from mixins.gen_load_finite import GenLoadFiniteBlob
from mixins.priority import LowPriority, HighPriority
from mixins.tasks import PeriodicTask
from taskset import TaskSet
import logging
from time import sleep

logging.basicConfig(level=logging.DEBUG)


class SpecialTask(PeriodicTask, LowPriority, GenLoadFiniteBlob):
    pass

ts = SpecialTask().generate()


md = MultiDistributor(["192.168.1.1"], 1024, ping=False, distributor_class=StubDistributor)
md.start(ts)


while True:
    for a in md:
        print(a)
        sleep(1)




