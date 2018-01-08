import xmltodict
from collections.abc import Iterable
from abc import ABCMeta, abstractmethod
import itertools
import random

from taskgen.task import Task




class TaskSet(Iterable):
    def __init__(self, tasks=[]):
        self._tasks = tasks
        self._task_counter = 0

    def __iter__(self):
        return self._tasks.__iter__()
    
    def __str__(self):
        return self._tasks.__str__()
        
    def append(self, task):
        task.id = self._task_counter
        self._task_counter += 1
        self._tasks.append(task)

    def variants(self):
        tasks_iters = map(lambda x: x.variants(), self._tasks)
        for tasks_variant in itertools.product(*tasks_iters):
            yield TaskSet(list(tasks_variant))

    def description(self):
        return {
            "taskset" : {
                "periodictask" : self._tasks
            }
        }

    def binaries(self):
        return set(map(lambda x: x.binary(), self._tasks))

    

class BlockTaskSet(TaskSet):
    """
    A, B, C
    [ A1, A2], B, [ C1, C2, C3]
    = [ A1, B, C1], [A1, B, C2], 
    """
    def __init__(self, *block_combinations, task_class=Task, seed=None):
        super().__init__()
        random.seed(seed)
        
        # wrap every argument, which is not of type list, with a list-object:
        # example: x->[x]
        block_combinations = map(lambda x: [x] if not isinstance(x, list) else x,
                                 list(block_combinations))
        
        for blocks in itertools.product(*block_combinations):
            # create a task from the block combinations and append it to the
            # taskset
            task = task_class(*blocks)
            self.append(task)


