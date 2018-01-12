from taskgen.task import Task
from taskgen.taskset import TaskSet, BlockTaskSet
from taskgen.blocks import *


class Test0(TaskSet):

    def __init__(self):
        super().__init__()

        self.append( Task( {
            # default
            "id" : 1,

            # unknown
            "executiontime" : 1000,
            "criticaltime" : 2000,

            # scheduling policy
#            "priority" : 10, #Fixed_Priority
            "deadline" : 3000,

            # binary
            "quota" : "1M",
            "pkg" : "hey",
            "config" : {}
        }))

        self.append( Task( {
            # default
            "id" : 2,

            # unknown
            "executiontime" : 1000,
            "criticaltime" : 2000,

            "deadline" : 4000,
            
            # scheduling policy
 #           "priority" : 20, #Fixed_Priority

            # binary
            "quota" : "1M",
            "pkg" : "hey",
            "config" : {}
        }))


class Test1(TaskSet):

    def __init__(self):
        super().__init__()
        task = Task(
            hey.HelloWorld,  # fills `pkg`, `config`, `executiontime` and `quota`
            priority.Custom(100), # fills `priority`
            period.Custom(5) # fills period
        )
        self.append(task)
        

