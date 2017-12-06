Beside the `taskgen` command line tool, you have the possibility to use the
framework and its classes inside REPL or any other project.

# LogDistributor

The `LogDistributor` is a stub implementation for the low level communication
with a genode instance. Combined with the `MultiDistributor`, it helps you
debugging. Instead of sending all task-sets, the xml representation is printed
to stdout.

# SimpleDistributor

The `SimpleDistributor` represents the most simple implementation of a
distributor. It connects to one genode instance and processes one taskset. It is
able to start, stop, close and send live requests. Please do not use this
distributor directly, it only abstracts the low level communication for the more
advanced `MultiDistributor`.

# MultiDistributor

The `MultiDistributor` is the default distributor for communication with
multiple genode instances. 

TODO


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

# Custom Task (with Mixins)

If you need a specific task, you do not need to redefine all behaviors. Specific
behaviors, like a high priority, are summarized in building blocks, called
mixins. They are located in the [mixins](../mixins) directory.  Further more
there are three types of base classes: `task.PeriodicTask`, `task.SporadicTask`
and `task.AperiodicTask`, which serve as starting point for your customization.

```
from taskgen.mixins.priority import HighPriority
from taskgen.mixins.gen_load_finite import GenLoadFinite
from taskgen.task import PeriodicTask

class MyTask(HighPriority, GenLoadFinite, PeriodicTask):
    pass
```

Now, this task can be appended in our custom task-set.

```
ts_4 = TaskSet()
ts_4.append( MyTask())
```

Keep in mind, that the base class is always listed at the rightmost class.

# Custom Task

Mixins are not the only way, how tasks can be created. The three task classes
`PeriodicTask`, `SporadicTask` and `AperiodicTask` are subtypes of the abstract
`Task` class. The `Task` class inherits from the Python `dict` class. It means,
that all attributes of the tasks are accessed and altered with dictionary
methods.

``` 
from taskgen.task import PeriodicTask

t = PeriodicTask()
t['priority'] = 128
t['id'] = "hello_world"
...
```

Every attribute in the Task can be a single value or of type `Iterable`. It is
possible to define ranges `range(0,10)`, lists `[0,1,2,3]` or custom
[generators](https://wiki.python.org/moin/Generators). Multiple options for a
value results in multiple variants of a task and finally multiple variants of a
taskset. If you want to analyse, how a scheduler reacts to different values of
one or more tasks, this is your way to go.

```
from taskgen.task import PeriodicTask

t = PeriodicTask()
t['priority'] = range(1, 128) # generates 128 variants of the task

assert t.has_variants() True
```

When it comes to the transmission of a task-set to a genode instance, a `Task`
is translated to a xml representation. All dictionary attributes, even nested
dictionaries, are directly mapped to a xml element.




# Optimization

When a task-set processing starts, you are able to handle over an optimization
goal. These optimization goals are represented with subclasses of the
`Optimization` class, which are located in the [optimizations](../optimizations) directory. 

```
from taskgen.optimization.fairness import Fairness
from taskgen.tasksets.example import ExampleTaskSet
from taskgen.distributors.multi_distributor import MultiDistributor

ts = ExampleTaskSet()
md = MultiDistributor("172.25.0.1", 1234)

# optimize fairness 
opt = Fairness()
md.start(ts, opt)
```

# Live Request Handlers

All data from a genode instance are pulled with *live* requests. The result of a
*live* request is represented with the `LiveResult` class. Live Request Handlers
handle `LiveResult`s and for example stores them to sqlite databases. Live
Handlers implementations are in the [lives](../lives) directory.

```
from taskgen.lives.sqlite import SQLiteLiveHandler
from taskgen.tasksets.example import ExampleTaskSet
from taskgen.distributors.multi_distributor import MultiDistributor

md = MultiDistributor("172.25.0.1", 1234)

# save all live requests to a sqlite db.
md.live_handler = SQLiteLiveHandler("./live.db")

ts = ExampleTaskSet()
md.start(ts, opt)
```
