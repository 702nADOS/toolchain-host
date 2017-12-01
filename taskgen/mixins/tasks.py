from .mixin import MixinMeta,Mixin
from collections.abc import Mapping
from abc import ABCMeta
import flatdict
import itertools
from taskset import TaskSet
from collections import Iterable

class CombinedMeta(ABCMeta, MixinMeta):
    pass

class Task(Mapping, Mixin, metaclass=CombinedMeta):
    _task = {
        # default values
        "id" : "test",
        "numberofjobs" : None,
        "priority" : None,
        "deadline" : None,

        # blob values
        "quota" : None,
        "pkg" : None,
        "config" : None
    }

    def __init__(self, *mixins):
        __bases__ = mixins
    
    def is_runnable(self):
        for value in self._task.values():
            if value == None:
                return False
            elif type(value) is dict:
                if not self.is_runnable(value):
                    return False
        return True

    
    def __getitem__(self, key):
        return self._task[key]

    def __iter__(self):
        return iter(self._task)

    def __len__(self):
        return len(self._task)    

    def generate(self):
        flat = flatdict.FlatDict(dict(self._task))

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
            yield TaskSet({"taskset" : flat.as_dict()})
            
    
class PeriodicTask(Task):
    _task = {
        "period" : None,
        "offset" : None
    }

class SporadicTask(Task):
    _task = {
        "inter_arrival" : None
    }

    
class AperiodicTask(Task):
    _task = {
        "inter_arrival" : 0
    }

