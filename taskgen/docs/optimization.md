# Optimization

When a task-set processing starts, you are able to handle over an optimization
goal. These optimization goals are represented with subclasses of the
`Optimization` class, which are located in the [optimizations](../optimizations) directory. 

```Python3
from taskgen.optimization import Optimization

class Fairness(Optimization):
    """ Fairness Optimization class exmaple"""
    def __init__(self):
        super().__init({
            "optimize" : {
                "goal" : {
                    "fairness" : {
                        "apply" : 1
                    },
                    "utilization" : {
                        "apply" : 0
                    }
                },
                "query_interval" : 1000
            }
        })
        
```
