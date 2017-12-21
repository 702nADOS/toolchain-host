from taskgen.task import Task
from taskgen.taskset import TaskSet, AttributeTaskSet
from taskgen.attrs import *
        
class Hey0TaskSet(TaskSet):
    """Static task with the `hey` binary. 
    
    It is possible to create a task from a dictionary. All values from the dict
    are mapped directly to a xml represenation.
    """
    def __init__(self):
        super().__init__()
        task = Task({
            "id" : 1,
            "executiontime" : 10000,
            "criticaltime" : 2000,
            "priority" : 10,
            "period" : 1000,
            "numberofjobs" : 3,
            "quota" : "1M",
            "pkg" : "hey",
            "config" : {}
        })
        self.append(task)


class Hey1TaskSet(TaskSet):
    """Static task with the `hey` binary.
    
    Attributes, defined in `taskgen.attrs` simplifies the task
    creation. Attributes are dicts with predefined values.
    """

    def __init__(self):
        super().__init__()
        task = Task(
            hey.HelloWorld,  # fills `pkg`, `config`, `executiontime` and `quota`
            priority.Custom(100), # fills `priority`
            period.Custom(5) # fills period
        )
        self.append(task)
        
class Hey2TaskSet(AttributeTaskSet):
    """Static task with the `hey` binary.
    
    If you want to create specific tasksets with the predefinied attributes,
    `AttributeTaskSet` might be helpful.
    """

    def __init__(self):
        super().__init__(
            hey.HelloWorld,
            priority.Custom(100),
            period.Custom(5)
        )


class Hey3TaskSet(AttributeTaskSet):
    """Two static tasks with the `hey` binary.
    
    `AttributeTaskSet` allows to combinate attributes. This example creates 2
    `hey`-tasks with various period.
    """

    def __init__(self):
        super().__init__(
            hey.HelloWorld,
            priority.Custom(100),
            [period.Custom(5), period.Custom(10)]
        )

        
class Hey4TaskSet(AttributeTaskSet):
    """Four static tasks with the `hey` binary, various periods and priorities.
    
    `AttributeTaskSet` allows to combinate attributes. This example creates 4
    `hey`-tasks with various period and priorities.
    """

    def __init__(self):
        super().__init__(
            hey.HelloWorld,
            [priority.Custom(100), priority.Custom(100)],
            [period.Custom(5), period.Custom(10)]
        )

        
class Hey5TaskSet(AttributeTaskSet):
    """One task with the `hey` binary and random priority.
    
    `AttributeTaskSet` allows to combinate random attributes. Random attributes
    are function, which returns randomly generated dicts.
    """

    def __init__(self):
        super().__init__(
            hey.HelloWorld,
            priority.Random,
            period.Custom(5)
        )

class Hey6TaskSet(AttributeTaskSet):
    """One task with the `hey` binary and all priority variants
    
    `AttributeTaskSet` allows to create variants of attributes. Variant
    attributes are function, which returns a dicts with value ranges. This
    example creates a taskset with one task and 128 variants, which all differ
    in the priority.
    """

    def __init__(self):
        super().__init__(
            hey.HelloWorld,
            priority.Variants,
            period.Custom(5)
        )

class Hey7TaskSet(AttributeTaskSet):
    """2 tasks with the `hey` binary, random period and all priority variants (2^128 variants).
    """

    def __init__(self):
        super().__init__(
            [hey.HelloWorld, hey.HelloWorld], # 2 tasks
            priority.Variants,  # 128 priority variants
            period.Random  #1-20 seconds periods
        )


class Hey8TaskSet(TaskSet):
    """10 static tasks with the `hey` binary.
    """

    def __init__(self):
        super().__init__()

        for x in range(10):
            task = Task(
                hey.HelloWorld,
                priority.Custom(100),
                period.Custom(5)
            )
            self.append(task)

            
class Hey9TaskSet(TaskSet):
    """10 tasks with the `hey` binary and random priorities.
    """

    def __init__(self):
        super().__init__()

        for x in range(10):
            task = Task(
                hey.HelloWorld,
                priority.Random,
                period.Custom(5)
            )
            self.append(task)

