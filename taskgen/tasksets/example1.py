from .mixins.tasks import *
from .mixins.priority import *
from .mixins.gen_load_finite import *

class Example1Taskset(PeriodicTask, LowPriority, GenLoadFiniteBlob):
    pass


