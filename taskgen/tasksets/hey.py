from taskgen.task import PeriodicTask
from taskgen.taskset import TaskSet

class Hey1Task(PeriodicTask):
    def __init__(self):
        super().__init__()
        self.update({
            "id" : 1,
            "executiontime" : 2000,
            "criticaltime" : 1000,
            "priority" : 128,
            "deadline" : 1000,
            "period" : 0,
            "numberofjobs" : 0,
            "offset" : 0,
            "quota" : "1M",
            "pkg" : "hey",
            "config" : {
                "arg1" : 126546
            }
        })

class Hey2Task(PeriodicTask):
    def __init__(self):
        super().__init__()
        self.update({
            "id" : 2,
            "executiontime" : 99999999,
            "criticaltime" : 0,
            "deadline" : 0,
            "priority" : 128,
            "period" : 0,
            "offset" : 0,
            "numberofjobs" : 0,
            "quota" : "1M",
            "pkg" : "hey",
            "config" : {
                "arg1" : 126546
            }
        })


class HeyTaskSet(TaskSet):
    def __init__(self):
        super().__init__()

        self.append(Hey2Task())
