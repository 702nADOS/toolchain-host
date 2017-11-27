from pprint import pprint as pp

import flatdict
import dicttoxml
from xml.dom.minidom import parseString



class Taskset:

    def produce(self):
        # right know, we only make use of one task. I indent to extend it by
        # multiple tasks.
        
        flat = flatdict.FlatDict(self._task)

        # make everything to an iterator, except iterators. By attention: strings are wrapped with an iterator again.
        iters = map(lambda x: [x] if not isinstance(x, collections.Iterable) or isinstance(x, str) else x, flat.itervalues())
        keys = flat.keys()

        for values in itertools.product(*iters):
            # update dictionary with the new combined values. This is done by
            # mapping all keys to their values.
            flat.update(dict(zip(keys, values)))
            xml = dicttoxml.dicttoxml(flat.as_dict(), custom_root='periodictask', attr_type=False)
            dom = parseString(xml)
            dom.toprettyxml())

