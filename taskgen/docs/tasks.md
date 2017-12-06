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
