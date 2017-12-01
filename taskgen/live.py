from abc import ABCMeta, abstractmethod


class AbstractLiveHandler(metaclass=ABCMeta):
    @abstractmethod
    def __handle__(self, taskset, live_result):
        pass
    
    def __get_delay__(self):
        return 5.0 # default, more than 5 second is not possible

    def __is_running__(self):
        return True
        

    
class SQLiteLiveHandler(AbstractLiveHandler):
    def __handle__(self, taskset, live_result):
        print live_result

    
        
class QueueLiveHandler(AbstractLiveHandler):
    def __handle__(self, taskset, live_result):
        print live_result
    


class LiveResult(MutableMapping):
    def __init__(self):
        self._optimization = None

    def dump(self):
        return xmltodict.unparse(self._optimization, pretty=True)

    def write(self, path):
        with open(path, 'a') as out:
            out.write(self.dump())

    def read(self, path):
        xml = open(path,'rb').read()
        self._optimzation = xmltodict.parse(xml)

    def __len__(self):
        return len(self._optimization)

    def __getitem__(self, ii):
        return self._optimization[ii]

    def __delitem__(self, ii):
        del self._optimization[ii]

    def __setitem__(self, ii, val):
        self._optimization[ii] = val

    def __str__(self):
        return str(self._optimization)

    def insert(self, ii, val):
        self._optimization.insert(ii, val)

    def append(self, val):
        self.insert(len(self._optimization), val)

    def __iter__(self):
        return iter(self._optimization)
