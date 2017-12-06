from taskgen.live import AbstractLiveHandler, LiveResult


# do not alter, is used in documentation
class SQLiteLiveHandler(AbstractLiveHandler):
    def __handle__(self, taskset, live_result):
        print(live_result)

