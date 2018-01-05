# Tasks

* basics
  * key-value pairs
  * dictionary
  

## Variants



## Attributes



# Basics

The three task classes `PeriodicTask`, `SporadicTask` and `AperiodicTask` are
subtypes of the abstract `Task` class and serve as starting point for your
customized task. The `Task` class inherits from the Python `dict` class.  All
attributes of a task are accessed and altered with dictionary methods.

```python3
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

```python3
from taskgen.task import PeriodicTask

t = PeriodicTask()
t['priority'] = range(1, 128) # generates 128 variants of the task

assert t.has_variants() True
```

# Xml mapping

When it comes to the transmission of a task-set to a genode instance, a `Task`
is translated to a xml representation. All dictionary attributes, even nested
dictionaries, are directly mapped to a xml element.
