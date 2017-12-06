# Basics

The three task classes `PeriodicTask`, `SporadicTask` and `AperiodicTask` are
subtypes of the abstract `Task` class and serve as starting point for your
customized task. The `Task` class inherits from the Python `dict` class.  All
attributes of a task are accessed and altered with dictionary methods.

```Python
from taskgen.task import PeriodicTask

t = PeriodicTask()
t['priority'] = 128
t['id'] = "hello_world"
...
```

# Variants

Every attribute in the Task can be a single value or of type `Iterable`. It is
possible to define ranges `range(0,10)`, lists `[0,1,2,3]` or custom
[generators](https://wiki.python.org/moin/Generators). Multiple options for a
value results in multiple variants of a task and finally multiple variants of a
taskset. If you want to analyse, how a scheduler reacts to different values of
one or more tasks, this is the way to go.

```Python
from taskgen.task import PeriodicTask

t = PeriodicTask()
t['priority'] = range(1, 128) # generates 128 variants of the task

assert t.has_variants() True
```

# Xml mapping

When it comes to the transmission of a task-set to a genode instance, a `Task`
is translated to a xml representation. All dictionary attributes, even nested
dictionaries, are directly mapped to a xml element.


# Mixins

If you need a specific task, you do not have to redefine all behaviors again and
again. Specific behaviors, like a high priority, are summarized in building
blocks, called mixins. They are located in the [mixins](../mixins) directory.


```Python
from taskgen.mixins.priority import HighPriority
from taskgen.mixins.gen_load_finite import GenLoadFinite
from taskgen.task import PeriodicTask

class MyTask(HighPriority, GenLoadFinite, PeriodicTask):
    pass
```

Now, this task can be appended to a task-set instance.

```Python
ts_4 = TaskSet()
ts_4.append( MyTask())
```

Keep in mind, that the base class is always listed as the rightmost
class.

