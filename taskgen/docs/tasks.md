# Tasks

`Task` is subclass of Python's `dict` and therefore behaves the same way. All
attributes of a task are accessed and altered with dictionary methods. 

```Python
from taskgen.task import Task

task = Task()
task['priority'] = 128
task['id'] = 0

# or

task_dict = {
    'priority' : 128,
    'id' : 0
}

task = Task(task_dict)
```

It is possible to build a `Task` from multiple dictionary objects. This concept
is named task blocks and described in [Task-Blocks](./blocks.md).

## Variants

Every attribute in the Task can be a single value or of type `Iterable`. It is
possible to define ranges `range(0,10)`, lists `[0,1,2,3]` or custom
[generators](https://wiki.python.org/moin/Generators). Multiple options for a
value results in multiple variants of a task and finally multiple variants of a
taskset. If you want to analyse, how a scheduler reacts to different values of
one or more tasks, this is the way to go.

```Python
from taskgen.task import Task

task = Task()
task['id] = range(0,100)
task['priority'] = 42

for variant in task.variants(): # generates 128 variants of the task
    print(variant)
```

## Attributes

Following attributes are part of every task.

### General

| Key | Type | Description |
| --- | --- | --- |
| `id` | Integer | Every task is identifed by an unique ID. |

### Binary

| Key | Type | Description |
| --- | --- | --- |
| `quota` | Integer | todo |
| `pkg` | String | todo |
| `config` | `dict` | todo |

### Frequency

| Key | Type | Description |
| --- | --- | --- |
| `period` | Integer | todo |
| `numberofjobs` | Integer | todo |

### Schedulability

| Key | Type | Description |
| --- | --- | --- |
| `priority` | Integer | todo |

or

| Key | Type | Description |
| --- | --- | --- |
| `deadline` | Integer | todo |

### Unknown

| Key | Type | Description |
| --- | --- | --- |
| `criticaltime` | Integer | todo |
| `executiontime` | Integer | todo |



