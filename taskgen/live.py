from abc import ABCMeta, abstractmethod
import xmltodict
import logging

class AbstractLiveHandler(metaclass=ABCMeta):

    # return: False for not running anymore
    #         True for still running, continue
    @abstractmethod
    def __handle_request__(self, taskset, live_xml):
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

    @abstractmethod
    def __get_delay__(self):
        pass

class DefaultLiveHandler(AbstractLiveHandler):
    def __init__(self):
        self._logger = logging.getLogger("DefaultLiveHandler")
    
    def __handle_request__(self, taskset, live_xml):
        taskset.counter += 1
        try:
            live_dict = xmltodict.parse(live_xml)
            tasks = live_dict['live']['task-descriptions']['task']
            self._logger.debug("successfully parsed result of live request")
        except:
            self._logger.critical("unable to parse live request result.")

        # cancel taskset after 5 live requests
        return taskset.counter < 5
    
    def __taskset_start__(self, taskset):
        taskset.counter = 1

    def __taskset_finish__(self, taskset):
        pass

    def __taskset_stop__(self, taskset):
        pass

    def __get_delay__(self):
        # send a request every 5 seconds
        return 5.0

