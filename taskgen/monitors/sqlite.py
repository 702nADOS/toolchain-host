from taskgen.monitor import DefaultMonitor

class YourHandler(DefaultMonitor):

    def __init__(self):
        super().__init__()
        # YOUR implementation
        
    def __taskset_event__(self, taskset, event):
        running = super().__init__(taskset, event)

        # YOUR implementation
        
        return running
    
    def __taskset_start__(self, taskset):
        # YOUR implementation
        pass

    def __taskset_finish__(self, taskset):
        # YOUR implementation
        pass

    def __taskset_stop__(self, taskset):
        # YOUR implementation
        pass




