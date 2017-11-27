import sys
from collections.abc import MutableSequence
import flatdict
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
from mixins.tasks import Task
import itertools
from collections import Iterable

# debugging
from pprint import pprint as pp

class TaskSet(MutableSequence):
    
    def __init__(self, data=None):
        if (data is not None):
            self._tasks = list(data)
        else:
            self._tasks = list()

    def __repr__(self):
        return "<{0} {1}>".format(self.__class__.__name__, self._tasks)

    def __len__(self):
        return len(self._tasks)

    def __getitem__(self, ii):
        return self._tasks[ii]

    def __delitem__(self, ii):
        del self._tasks[ii]

    def __setitem__(self, ii, val):
        self._acl_check(val)
        self._tasks[ii] = val

    def __str__(self):
        return str(self._tasks)

    def insert(self, ii, val):
        self._acl_check(val)
        self._tasks.insert(ii, val)

    def append(self, val):
        self.insert(len(self._tasks), val)

    def _acl_check(self, val):
        if not isinstance(val, Task):
            raise TypeError(v)

    def produce(self):
        # TODO right know, we only make usage of one task. I indent to extend it
        # by multiple tasks.
        if len(self._tasks) == 0:
            return
        flat = flatdict.FlatDict(dict(self._tasks[0]))

        # make everything to an iterator, except iterators. Pay attention:
        # strings are wrapped with an iterator again.
        iters = map(lambda x: [x] if not isinstance(x, Iterable) or
                    isinstance(x, str) else x, flat.itervalues())
        keys = flat.keys()

        # generator
        for values in itertools.product(*iters):
            # update dictionary with the new combined values. This is done by
            # mapping all keys to their values.
            flat.update(dict(zip(keys, values)))
            xml = dicttoxml(flat.as_dict(), custom_root='periodictask',
                            attr_type=False)
            dom = parseString(xml)
            yield dom.toprettyxml()

            
    def export(self, path, prefix="taskset"):
        for index, xml_data in enumerate(self.produce()):
            ts_path = path + "/" + prefix + "_" + str(index) + ".xml"
            with open(ts_path, 'a') as out:
                out.write(xml_data)
