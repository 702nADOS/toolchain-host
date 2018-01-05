from abc import ABCMeta, abstractmethod
import xmltodict
import logging
import random


class AbstractMonitor(metaclass=ABCMeta):

    # return True: if continue running
    #        False: if stop running
    @abstractmethod
    def __taskset_event__(self, taskset, event):
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


class DefaultMonitor(AbstractMonitor):

    def __init__(self):
        self.logger = logging.getLogger("DefaultMonitor")


    def _get_task_by_id(self, taskset, task_id):
        # the taskset is a list, we have to loop over all items...
        for task in taskset:
            if task.id == task_id:
                return task
        return None

    def __taskset_event__(self, taskset, profile):
        try:
            events = profile['profile']['events']['event']
        except:
            self.logger.critical("'profile'-node of event has unknown structure"+
                                 " and can not be parsed. TaskSet stopped.")
            return False
        
        for event in events:
            try:
                _task_id = int(event['@task-id'])
                _type = event['@type']
                _timestamp = int(event['@time-stamp'])
            except:
                self.logger.critical("'task'-node of event has unknown structure"+
                                     " and can not be parsed. TaskSet stopped.")
                return False

            # find task
            task = self._get_task_by_id(taskset, _task_id)
            
            # update task
            task.events[_type] = _timestamp
            
        # check whether any task is running
        is_running = lambda task: 'EXIT' not in task.events
        running = map(is_running, taskset)
        return any(running)

    def __taskset_start__(self, taskset):
        pass

    def __taskset_finish__(self, taskset):
        pass

    def __taskset_stop__(self, taskset):
        pass
