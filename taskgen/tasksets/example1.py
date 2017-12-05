from .tasks import *
from .mixins.priority import *
from .mixins.gen_load_finite import *
from .taskset import TaskSet

class TaskA(PeriodicTask, LowPriority, GenLoadFiniteBlob):
    pass

class TaskB(PeriodicTask, GenLoadFiniteBlob):
    pass


class Example1TaskSet(TaskSet):
    """A simple example class"""
    def __init__(self):
        super().__init__()

        self.append(TaskA())
        self.append(TaskB())
        self.append(TaskA())

class Example2TaskSet(TaskSet):
    """Another example taskset"""
    def __init__(self):
        super().__init__()

        self.append(TaskB())
        self.append(TaskA())
