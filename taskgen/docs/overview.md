Components of taskgen
=====================
  
* [**Task**](tasks.md) A Task consists of key-value pairs, which describes
  the behavior of a real-time capable process. One key could be `priority` and
  its associated value might be `25`. Tasks are implemented as python
  dictionaries.  
  
* [**Attributes**](attributes.md) are building blocks for a task and are
  represented with key-value pairs, too.  An Attribute is a dictionary object or
  a function which returns a dictionary object.  
  
* [**Task-Sets**](taskset.md) are containers for tasks.  

* [**Optimization**](optimization.md) classes contains optimization goals
  for a task-set. Optimizations are represented by python dictionaries.  
  
* [**Event Handlers**](event.md) handle occuring events. An event is fired,
  whenever a task processing starts or ends.  
  
* [**Distributor**](distributor.md) sends a task-set and its optimization
  goal to a platform, which is able to execute task-sets. The low level
  connection to such a platform is realized with a **Session**.  
  
* [**Sessions**](session.md) contain the low level implementations for
  sending task-sets, optimization classes and for receiving events.  
  

General Workflow
================

1. Choose a task-set class
2. Optionally choose a optimization class
3. Optionally choose an event handler
4. Optionally choose a session for a target platform.
5. Start sending and processing task-set.

These steps can be done by using the [command line tool](commandline.md) or
by writing a python script and using the module's classes:

```Python
from taskgen.tasksets.hey import Hey1TaskSet
from taskgen.distributor import Distributor
from taskgen.optimizations.fairness import Fairness

taskset = Hey1TaskSet()
optimization = Fairness()

distributor = Distributor("172.25.1.2")
distributor.start(taskset, optimization)
```

For more comprehensive examples read the [documentation](.) and look at the
[scripts](../scripts/) folder, please.

