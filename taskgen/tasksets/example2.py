from .mixins.tasks import *
from .mixins.priority import *
from .mixins.gen_load_finite import *

class Example2Taskset(PeriodicTask, LowPriority, GenLoadFiniteBlob):
    pass

class Example3Taskset(PeriodicTask, LowPriority, GenLoadFiniteBlob):
    pass



