from .mixin import Mixin

class HighPriority(Mixin):
    _task = {
        "priority" : range(300, 400)
    }

    def __str__(self):
         return "Priority betwen 300 and 400"

class LowPriority(Mixin):
    _task = {
        "priority" : range(0,10)
    }

    def __str__(self):
         return "Priority betwen 300 and 400"
