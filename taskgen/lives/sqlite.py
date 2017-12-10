from taskgen.live import DefaultLiveHandler


# do not alter, is used in documentation
class SQLiteLiveHandler(DefaultLiveHandler):

    def __init__(self):
        super().__init__()
        

    def __taskset_start__(self, taskset):
        super().__taskset_start__()
        

    def __taskset_finish__(self, taskset):
        super().__taskset_finish__()
        pass

    def __taskset_stop__(self, taskset):
        super().__taskset_stop__()
        pass

    def __prehandled_request__(self, taskset, task_descriptions):
        pass


