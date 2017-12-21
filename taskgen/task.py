from collections.abc import Mapping
from abc import ABCMeta, abstractmethod
import flatdict
import itertools
from collections import Iterable
import flatdict

#class CombinedMeta(ABCMeta, MixinMeta):
#    pass

class Task(dict):
    def __init__(self, *attrs):
        super().__init__({
            # default values
            "id" : None,
            "priority" : None,

            # blob values
            "quota" : None,
            "pkg" : None,
            "config" : None,

            # periodic task
            "period" : None,
            
            "numberofjobs" : 1
            # "offset" : None, unused at genode side.
        })

        # add inital attributes
        for attr in attrs:
            if callable(attr):
                attr = attr()
#            if not isinstance(attr, dict):
#                raise ValueError("An attribute for a task must be dict.")
            super().update(attr)


    def variants(self):
        flat = flatdict.FlatDict(self,None, dict,True)

        # make everything to an iterator, except iterators. Pay attention:
        # strings are wrapped with an iterator again.
        iters = map(lambda x: [x] if not isinstance(x, Iterable) or
                    isinstance(x, str) else x, flat.itervalues())
        keys = flat.keys()
        
        for values in itertools.product(*iters):
            # update dictionary with the new combined values. This is done by
            # mapping all keys to their values.
            flat.update(dict(zip(keys, values)))
            
            # create new task
            yield Task(flat.as_dict())

    def binary(self):
        return self['pkg']
            
    
