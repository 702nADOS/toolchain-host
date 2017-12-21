Components of taskgen
=====================
  
* [**Task**](docs/tasks.md) A Task consists of key-value pairs, which describes
  the behavior of a real-time capable process. One key could be `priority` and
  its associated value might be `25`. Tasks are implemented as python
  dictionaries.
* [**Attributes**](docs/attributes.md) are building blocks for a task and are
  represented with key-value pairs, too.  An Attribute is a dictionary object or
  a function which returns a dictionary object.
* [**Task-Sets**](docs/taskset.md) are containers for tasks.
* [**Optimization**](docs/optimization.md) classes contains optimization goals
  for a task-set. Optimizations are represented by python dictionaries.
* [**Event Handlers**](docs/event.md) handle occuring events. An event is fired,
  whenever a task processing starts or ends.
* [**Distributor**](docs/distributor.md) sends a task-set and its optimization
  goal to a platform, which is able to execute task-sets. The low level
  connection to such a platform is realized with a **Session**.
* [**Sessions**](docs/session.md) contain the low level implementations for
  sending task-sets, optimization classes and for receiving events.
  

General Workflow
================

1. Choosing a task-set class
2. Optionally choosing a optimization class
3. Optionally choosing an event handler
4. Optionally choosing a session for a target platform.
5. Start sending and processing task-set.

These steps can be done by using the [command line tool](docs/commandline.md) or
by writing a python script and using the module's classes:

```Python3
from taskgen.tasksets.hey import Hey1TaskSet
from taskgen.distributor import Distributor
from taskgen.optimizations.fairness import Fairness

taskset = Hey1TaskSet()
optimization = Fairness()

distributor = Distributor("172.25.1.2")
distributor.start(taskset, optimization)
```

For more comprehensive examples read the [documentation](docs/) and look at the
[scripts](scripts/) folder, please.

