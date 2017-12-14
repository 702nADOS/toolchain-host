from collections.abc import Mapping
from abc import ABCMeta, abstractmethod
import flatdict
import itertools
from collections import Iterable


#class CombinedMeta(ABCMeta, MixinMeta):
#    pass

class Task(dict):
    def __init__(self):
        super().__init__()
        super().update( {
            # default values
            "id" : None,
            "priority" : None,

            # blob values
            "quota" : None,
            "pkg" : None,
            "config" : None,

            # periodic task
            "period" : None,

            # "offset" : None, unused at genode side.
            
        })

    def __key__(self):
        return "periodictask"
        
    def _iterate_dict(self, d, f):
        if isinstance(d, dict):
            return any([self._iterate_dict(k, f) for k in d])
        else:
            return f(self[d])
        
#    def is_complete(self):
#        # searches for None in _task
#        return not self._iterate_dict(self, lambda x: x is None)

#    def has_variants(self):
        # searches for Iterable in _task and ignores strings
#        return self._iterate_dict(self, lambda x: isinstance(x, Iterable)
#                                   and not isinstance(x, str))
 
    
"""
# Not supported and implemented at genode side.

class SporadicTask(Task):
    def __init__(self):
        super().__init__()
        super().update( {
            "inter_arrival" : None
        })

    def __key__(self):
        return "sporadictask"



    
class AperiodicTask(Task):
    def __init__(self):
        super().__init__()
        super().update( {
            "inter_arrival" : 0
        })

    def __key__(self):
        return "aperiodictask"
"""
