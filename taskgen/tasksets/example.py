from taskgen.task import Task
from taskgen.mixins.priority import LowPriority
from taskgen.mixins.gen_load_finite import GenLoadFinite
from taskgen.taskset import TaskSet


# DO NOT DELETE, is an exmaple for the documentation
class ExampleTask(LowPriority, GenLoadFinite, Task):
    pass




# TO NOT DELETE, is an example for the documentation
class ExampleTaskSet(TaskSet):
    """A simple example class"""
    def __init__(self):
        super().__init__()

        self.append(ExampleTask())


class HugeTaskSet(TaskSet):
    """A simple example class"""
    def __init__(self):
        super().__init__()

        for x in range(0, 10000):
            self.append(ExampleTask())
        
