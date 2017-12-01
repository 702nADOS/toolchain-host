# todos
- [ ] Distributors
  - [ ] MultiDistributor
    - [x] Implementation
    - [x] Refactoring
    - [ ] Documentation
  - [ ] ScanDistributor
    - [x] Implementation
    - [x] Refactoring
    - [ ] Documentation
  - [ ] SimpleDistributor
    - [x] Implementation
    - [x] Refactoring
    - [ ] Documentation
- [ ] TaskSet
  - [x] Proof-Of-Concept Implementation
  - [ ] Full Implementation
  - [ ] Documentation
- [ ] Mixins
  - [x] Proof-Of-Concept Implementation
  - [ ] Documentation
  - [ ] Classes
    - [x] Tasks
    - [ ] Priority
    - [ ] Sizes
- [ ] Examples
- [ ] Unit Tests
- [ ] Makefile Integration
- [ ] Genode Implementation
  - [ ] Sporadic Tasks
  - [ ] Asyncron Tasks
    
# Dynamic TaskSet generation with Mixins 

There are several reasons for using Mixins as main feature for creating
tasksets. On one side, we do not need to provide a lot of boilercode. At the
other side, you are able to to extend the TaskSet functionality by just writing
another Mixin class.  New tasksets are created by just extending the TaskSet
base class with Mixins.  Finally the GUI Application doens't need an update
after new functionality is added to the framework, because it will have the
capability for searching after Mixins and listing them as directory tree.

Mixins might be:
* LargeSet *large number of Tasks*
* SmallSet *small number of Tasks*
* MediumSet *medium number of Tasks*
* PeriodicTask *extends the TaskSet with periodic tasks*
* SporadicTask
* AsyncronTask
* HeyBlob *extends the tasks with the Hey Binary*
* IdleBlob *another binary as Mixin*

Further research is needed for a good Set of Mixins.

## Mixin Tree

* mixins
  * blobs
    * hey
      * ExtremHeyBlobMixin
      * DefaultHeyBlobMixin
    * Idle
    * Namste
    * tumatmul
  * tasks
    * PeriodicTaskMixin
    * AperiodicTaskMixin
    * SporadicTaskMixin
  * size
    * SmallSetMixin
    * MediumSetMixin
    * LargeSetMixin
  * priority
    * HighPriorityMixin
    * LowPriorityMixin
    * MediumPriorityMixin

## How to prevent Overwrites by other mixins 

A small dictionary check implemented in the BaseTaskset will prevent collision
of mixins. This allows also exclusive mixins, which might be useful for mixins
like SporadicTask and AperiodicTask. Both mixins at the same time doesnt make
sense.

# Lazy Evaluation & Iterators

Lazy Evaluation make the generation of really huge TaskSets possible. Right now,
I intend to make use of the Pythons' Generator & Iterator paddern and
[itertools](https://docs.python.org/2/library/itertools.html), which supports
lazy evaluation. Of course, all attributes of a TaskSet Object like Period or
NumberOfTasks are accessible by Getter & Setter methods. Furthmore, there will
be filtering Mixins for limiting the size of tasksets. 

## Technical View
After adding the Mixins to the BaseTaskSet, the custom TaskSet contains a
dictionary with the structur of a xml task. It also keeps all Iterators of the
values. A cartesian product of all Iterators will generate a lazy-evaluated
tuple list. Each tuple is an actual task of the xml taskset.

# Python as Configuration

Beside Python, there are other ways to create configuration files for mixins:
* YAML
* XML
* JSON
All these formats do have several disadvantages: 
1. a lot of code for parsing need to be implemented. Error-prone.
2. Raising errors are linked to the parser code, but not to the actual mistake
   inside the configuration file.
3. Only predefined functionality is available. For example, new Iterators are
   not possible.

This small snippet creates a new Blob Mixin:
```
class DefaultHeyBlobMixin:
     description = "A default Hey. Tests the hey."
    _taskset = {
         "blob" : "hey",
         "params" : {
              "param1" : xrange(1, 5),
              "param2" : "hello"
         }
    }
```

# Usage and the SimpleDistributor component

```
from blob import HeyBlob
from mixins import *
from distributor import SimpleDistributor
class MyTaskSet(TaskSet, SporadicTask, LargeSet, HeyBlob):
    pass
    
ts = MyTaskSet()
ts.period = xrange(100, 124)

sd = SimpleDistributor("127.0.0.1", 3000)
sd.send(ts)
```

# ScanDistributor

```
def callback(ip, port, status):
    print ip, port, status
    
s = ScanDistributor("127.0.0.*", range(2000,3000))
s.scan(callback)
print s.available()
s.send(ts)
```

# Dynamic taskset adjustment
```
c = TaskSet()
c.__bases__ += hey, periodic

s = SimpleDistributor("127.0.0.1", 3000)

for period in range(1, 10):
    s.send(c)
    s.recv()
    
    # make adjustments to c
    # machine learning might help...
    c.period = period
```
