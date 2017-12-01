from abc import ABCMeta, abstractmethod
from collections.abc import MutableMapping

class AbstractLiveHandler(metaclass=ABCMeta):
    @abstractmethod
    def __handle__(self, taskset, live_result):
        pass
    
    def __get_delay__(self):
        return 5.0 # default, more than 5 second is not possible

    
class SQLiteLiveHandler(AbstractLiveHandler):
    def __handle__(self, taskset, live_result):
        print(live_result)

    
        
class QueueLiveHandler(AbstractLiveHandler):
    def __handle__(self, taskset, live_result):
        print(live_result)

class LiveResult(MutableMapping):
    def __init__(self, live = None):
        self._live = live

    def dump(self):
        return xmltodict.unparse(self._live, pretty=True)

    def write(self, path):
        with open(path, 'a') as out:
            out.write(self.dump())

    def __is_running__(self):
        return self._live['running']
            
    def read(self, path):
        xml = open(path,'rb').read()
        self._optimzation = xmltodict.parse(xml)

    def __len__(self):
        return len(self._live)

    def __getitem__(self, ii):
        return self._live[ii]

    def __delitem__(self, ii):
        del self._live[ii]

    def __setitem__(self, ii, val):
        self._live[ii] = val

    def __str__(self):
        return str(self._live)

    def insert(self, ii, val):
        self._live.insert(ii, val)

    def append(self, val):
        self.insert(len(self._live), val)

    def __iter__(self):
        return iter(self._live)
