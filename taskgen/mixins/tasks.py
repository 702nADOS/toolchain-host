from .mixin import MixinMeta,Mixin
from collections.abc import Mapping
from abc import ABCMeta

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

