from abc import ABCMeta, abstractmethod


# we need some conventions, to ensure that the MultiDistributor is working
class AbstractDistributor(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, host, port):
        pass
    
    @abstractmethod
    def start(self, optimization, taskset):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def live_request(self):
        pass

    @abstractmethod
    def close(self):
        pass
