# Predefined TaskSet

Task-Sets are all located inside the [tasksets](../tasksets/) directory. Each
Task-Set is represented as subclass of `TaskSet`. Task-Sets can be runnable
out-of-the-box if there are no constructor parameters. For example, the
`tasksets.example.ExampleTaskSet` implementation does not need further parameters.

```
from taskgen.tasksets.example import ExampleTaskSet
from taskgen.distributors.multi_distributor import MultiDistributor

ts = ExampleTaskSet()

md = MultiDistributor("172.25.0.1", 1234)
md.start(ts)
```

# Custom TaskSet

The Usage of task-sets is not limited to predefined implementations. It is
possible to build your custom task-set by using the base `taskset.TaskSet` class
and append your `Task` classes. The `tasksets.example.ExampleTask` is reused for
this example.

```
from taskgen.tasksets.example import ExampleTask
from taskgen.taskset import TaskSet

ts_1 = TaskSet()

# add one ExampleTask object
ts_1.append( ExampleTask())
# add another ExampleTask object
ts_1.append( ExampleTask())
```

You can concatenate tasksets:

```
ts_2 = TaskSet()
ts_2.append( ExampleTask())

ts_all = ts_1 + ts_2
```

Keep in mind, that the `TaskSet` does not behave like a list or dictionary. Only
the append and concatenation-operator are supported. This has some performance
reasons. Read the pydocs for further function definitions.

# TaskSet Variants

Tasks can store multiple values for one attribute. These leads to multiple
variants of a Task and finally multiple variants of a TaskSet. There is no way to
determine the actual number of variants, only if it has variants
`TaskSet.has_variants()`. It also can have infinite variants, which will keep
the distributor running.

