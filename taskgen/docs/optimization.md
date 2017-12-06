# Optimization

When a task-set processing starts, you are able to handle over an optimization
goal. These optimization goals are represented with subclasses of the
`Optimization` class, which are located in the [optimizations](../optimizations) directory. 

```python3
from taskgen.optimization.fairness import Fairness
from taskgen.tasksets.example import ExampleTaskSet
from taskgen.distributors.multi_distributor import MultiDistributor

ts = ExampleTaskSet()
md = MultiDistributor("172.25.0.1", 1234)

# optimize fairness 
opt = Fairness()
md.start(ts, opt)
```
