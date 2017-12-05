from .mixin import MixinMeta,Mixin
from collections.abc import Mapping
from abc import ABCMeta, abstractmethod
import flatdict
import itertools
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

    def __init__(self, task = {}):
        self._task = task
    
    @abstractmethod
    def __key__(self):
        pass

    def __str__(self):
        return dict(self._task
    
    def _iterate_dict(self, d, f):
        if isinstance(d, dict):
            return any([self._dict_has_type(k, f) for k in d])
        else:
            return f(d)
        
    def is_runnable(self):
        # searches for None in _task
        return not self._iterate_dict(self._task, lambda x: isinstance(x, None))

    def has_variants(self):
        # searches for Iterable in _task and ignores strings
        return self._dict_has_type(self._task, lambda x: isinstance(x, Iterable)
                                   and not isinstance(x, str))
    
    def __getitem__(self, key):
        return self._task[key]

    def __iter__(self):
        return iter(self._task)

    def __len__(self):
        return len(self._task)    

    
class PeriodicTask(Task):
    _task = {
        "period" : None,
        "offset" : None
    }

    def __key__(self):
        return "periodictask"

class SporadicTask(Task):
    _task = {
        "inter_arrival" : None
    }

    def __key__(self):
        return "sporadictask"

    
class AperiodicTask(Task):
    _task = {
        "inter_arrival" : 0
    }

    def __key__(self):
        return "sporadictask"

