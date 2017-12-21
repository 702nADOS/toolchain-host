import xmltodict
from collections.abc import MutableSequence
from abc import ABCMeta, abstractmethod
import itertools
import random

from taskgen.task import Task




class TaskSet:
    def __init__(self, tasks=[]):
        self._tasks = tasks
        self._cached_xml = None 
        
    def __str__(self):
        return self._tasks.__str__()
        
    def append(self, task):
        self._tasks.append(task)

    def variants(self):
        tasks_iters = map(lambda x: x.variants(), self._tasks)
        for tasks_variant in itertools.product(*tasks_iters):
            yield TaskSet(list(tasks_variant))

    def description(self):
        if self._cached_xml is None:
            taskset = {"taskset" : {
                "periodictask" : self._tasks }
            }
            # genode can't handle `<?xml version="1.0" encoding="utf-8"?>` at
            # the documents beginning. `full_document=False` removes it.
            self._cached_xml = xmltodict.unparse(taskset,
                                                 pretty=True,
                                                 full_document=False)
        return self._cached_xml        

    def binaries(self):
        return map(lambda x: x.binary(), self._tasks)

    

class AttributeTaskSet(TaskSet):
    """
    A, B, C
    [ A1, A2], B, [ C1, C2, C3]
    = [ A1, B, C1], [A1, B, C2], 
    """
    def __init__(self, *attrs_combinations, task_class=Task, seed=None):
        super().__init__()
        random.seed(seed)
        
        # wrap every argument, which is not of type list, with a list-object:
        # example: x->[x]
        attrs_combinations = map(lambda x: [x] if not isinstance(x, list) else x,
                                 list(attrs_combinations))
        
        for attrs in itertools.product(*attrs_combinations):
            # create a task from the attribute combinations and append it to the
            # taskset
            task = task_class(*attrs)
            self.append(task)


