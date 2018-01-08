from abc import ABCMeta, abstractmethod

# we need some conventions, to ensure that the Distributor is working
class AbstractSession(metaclass=ABCMeta):

    @staticmethod
    def is_available(host):
        return True
    
    @abstractmethod
    def __init__(self, host, port):
        pass

    @abstractmethod
    def start(self, taskset, *params):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def event(self):
        pass

    @abstractmethod
    def close(self):
        pass
