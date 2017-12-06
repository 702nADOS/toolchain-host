# tasgen

taskgen is is a taskset generation framework for the
[genode-Taskloader](https://github.com/argos-research/genode-Taskloader)
component. 


# Goals
- **Easy extensibility** New modules like are simple to add as new classes. The
  primary classes `TaskSet` and `Task` are represented as dictionaries, which
  allows a direct mapping from `Task` attributes to the final xml
  representation.
  
- **Work with Python** No separate models configuration files in a declarative
  format. Models are described in Python code, which is compact, easier to
  debug, and allows for ease of extensibility
  
- **Large-Scale** TaskSet variants up to 1 billion or even infinite taskset
  generators are no problems. Lazy evaluation only generate as much tasksets as
  needed at runtime.
  
- **User friendly** Threading keeps waiting time low and work like ping,
  connect, processing tasksets is done in background. A fast-responsive
  framework is the result.

# Getting started

The core of taskgen are the the [task-sets](./tasksets/). This directory
contains abstract task-set generators and predefined out-of-the-box runnable
task-sets like `TODO`. For more complex task-set generation, you should us the
[taskgen functional API](api.md). Another helpful tool is the command
line application:

```
usage: __main__.py run [-h] [-v] [--log-file FILE] -p PORT -t CLASS [-l CLASS]
                       [-o CLASS] [--pretend]
                       IP [IP ...]
```

Beside a port and one or multiple IP, IP-ranges, a taskset is neccesary for
processing. A taskset can have variants, which is means, that some attributes
may have multiple values. Every variant is executed as single taskset at one
destination genode instance.
Now lets do same dry exercise and execute a taskset with its variants at
three destination instances. There is no need for real genode instances, the
`--pretend` flag replaces the actual connection by a stub.

```
./taskgen run --pretend -p 1234 -t TODO 172.25.0.1 172.25.0.2 172.25.0.3
```

# Documentation
* [Command line tool](docs/commandline.md)
* [Distributors](docs/distributors.md)
* [Task-Sets](docs/taskset.md)
* [Tasks](docs/tasks.md)
* [Mixins](docs/mixins.md)
* [Optimization](docs/optimization.md)
* [Live Request Handler](docs/live.md)


# Project layout

    docs/                         # documentation in markdown
    taskset.py                    # TaskSet base class implementation
    tasks.py                      # Periodic-, Sporadic-, AperiodicTask implementation
    live.py                       # live request handler implementations
    optimization.py               # base class for optimization
    distributors/
        simple_distributor.py     # genode distributor implementation
        multi_distributor.py      # advanced, asyncron, multi connection distributor
    mixins/                       # direcotry for mixins (task configurations)
        gen_load_finite.py        # binary configuration file
        ...
    tasksets/                     # directory for taskset classes
        ...
    lives/
        sqlite.py                 # live request handler with sqlite support
        ...
    optimizations/
        fairness.py               # optimize fairness
        
