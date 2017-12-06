import xmltodict
import os
from collections.abc import MutableSequence
from collections import defaultdict
import flatdict
import itertools
from collections import Iterable

from taskgen.task import Task

class TaskSet:
    def __init__(self, taskset = {}):
        self._taskset = defaultdict(list, taskset)
        self._cached_xml = None 

    def __str__(self):
        return self._taskset.__str__()
        
    def append(self, task):
        self._taskset[task.__key__()].append(task)

    def __iter__(self):
        return itertools.chain.from_iterable(self._taskset.values())
    
    def __add__(self,other):
        ts = TaskSet(self._taskset)
        for task in other:
            ts.append(task)
        return ts

    def has_variants(self):
        return any(map(lambda x: x.has_variants(), self))

    def is_runnable(self):
        return all(map(lambda x: x.is_runnable(), self))

    def variants(self):
        flat = flatdict.FlatDict(self._taskset,None, dict,True)

        # make everything to an iterator, except iterators. Pay attention:
        # strings are wrapped with an iterator again.
        iters = map(lambda x: [x] if not isinstance(x, Iterable) or
                    isinstance(x, str) else x, flat.itervalues())
        keys = flat.keys()

        # generator for [TaskSet]
        for values in itertools.product(*iters):
            # update dictionary with the new combined values. This is done by
            # mapping all keys to their values.
            flat.update(dict(zip(keys, values)))

            # create new taskset
            ts = TaskSet(flat.as_dict())
            yield ts
        
    def asxml(self):
        if self._cached_xml is None:
            taskset = {"taskset" : self._taskset}
            self._cached_xml = xmltodict.unparse(taskset, pretty=True)
        return self._cached_xml        



