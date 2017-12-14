import xmltodict
import os
from collections.abc import MutableSequence
from abc import ABCMeta, abstractmethod
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

#    def has_variants(self):
#        return any(map(lambda x: x.has_variants(), self))

#    def is_complete(self):
#        return all(map(lambda x: x.is_complete(), self))

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

            # create new taskset (pay attention: there are no references to a
            # Task object anymore, only dicts).
            yield TaskSet(flat.as_dict())

    def description(self):
        if self._cached_xml is None:
            taskset = {"taskset" : self._taskset}
            # genode can't handle `<?xml version="1.0" encoding="utf-8"?>` at
            # the documents beginning. `full_document=False` removes it.
            
            self._cached_xml = xmltodict.unparse(taskset, pretty=True, full_document=False )
        return self._cached_xml        

    def binaries(self):
        return [task['pkg'] for task in self]

