from abc import ABCMeta, abstractmethod
import xmltodict
import logging
import random


class AbstractEventHandler(metaclass=ABCMeta):
    
    @abstractmethod
    def __taskset_event__(self, taskset, event_xml):
        pass

    @abstractmethod
    def __taskset_start__(self, taskset):
        pass

    @abstractmethod
    def __taskset_finish__(self, taskset):
        pass

    @abstractmethod
    def __taskset_stop__(self, taskset):
        pass

def taskset_is_processing(event):
    return False #random.randint(0,4) == 0
