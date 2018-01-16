from taskgen.monitor import AbstractMonitor


class CsvMonitor(AbstractMonitor):

    def __init__(self, path="events.csv"):
        self._logger = logging.getLogger("CsvMonitor")

        
    def __taskset_event__(self, taskset, event):
        print(event)
    
    def __taskset_start__(self, taskset):
        pass

    def __taskset_finish__(self, taskset):
        pass

    def __taskset_stop__(self, taskset):
        pass




