"""Module for handling events

Target systems might send events containing information about the current
task-set processing.  Parsing incoming events is the main goal of a
monitor. Additional monitors can do further processing with these events, like
saving information to databases.

If you want to implement a Monitor for processing, the `DefaultMonitor` might be
the best starting point.

Keep in mind, that the methods are called by another threads than the main
thread. Due to this fact, you have to take care of multi threading by using
locks, semaphores, usw.

"""

from abc import ABCMeta, abstractmethod
import xmltodict
import logging
import random


class AbstractMonitor(metaclass=ABCMeta):
    """Most abstract monitor class.

    This class does not handle the desicion, if a task-set processing is
    finished or needs to continue. You have to implement it in
    `__taskset_events__` and return a bool.

    """
    # return True: if continue running
    #        False: if stop running
    @abstractmethod
    def __taskset_event__(self, taskset, event):
        """Called, whenever an event is received.
        
        :return: True, if the task-set is finished. Otherwise return False and
        the processing continues.
        :rtype: bool
        """
        pass

    @abstractmethod
    def __taskset_start__(self, taskset):
        """A task-set processing started"""
        pass

    @abstractmethod
    def __taskset_finish__(self, taskset):
        """A task-set processing is finished."""
        pass

    @abstractmethod
    def __taskset_stop__(self, taskset):
        """A task-set processing is canceled due to an error or is stopped regularly."""
        pass


class DefaultMonitor(AbstractMonitor):
    """Default class for monitors
    
    This monitor handles events and determinates the running status of a
    task-set.

    It is recommeded to inherit from this class for further monitors.

    """
    def __init__(self):
        self.logger = logging.getLogger("DefaultMonitor")


    def _get_task_by_id(self, taskset, task_id):
        # the taskset is a list, we have to loop over all items...
        for task in taskset:
            if task.id == task_id:
                return task
        return None

    def __taskset_event__(self, taskset, profile):
        """Determinates the running status of the current task-set.

        This is done by updating the event status of each task. If all tasks of
        a task-set have an `EXIT` event, the task-set is finished.

        """
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
