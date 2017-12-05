from .mixin import Mixin




class HighPriority:
    def __init__(self):
        super().__init__()
        super().update({
            "priority" : range(0,10)            
        })

class LowPriority:
    def __init__(self):
        super().__init__()
        super().update({
            "priority" : range(0,10)            
        })
