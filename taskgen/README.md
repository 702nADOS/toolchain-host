# taskgen

A taskset generation framework for the
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


# Installation

```
pip3 install --user -r ./requirements.txt
```


# Getting started
The core of taskgen is the distribution of task-sets to running
genode-Taskloader instances. taskgen is shipped with a command line tool.

Option 1:

```bash
cd ..
python3 -m taskgen --help
```

Option2:

```bash
./taskgen --help
```

Use the tool to list all available tasksets:

```bash
./taskgen list --taskset
```

We want to distribute the `example.ExampleTaskSet` task-set to one destination
instance. 

```bash
./taskgen run -d -t example.ExampleTaskSet -p 1234 172.25.0.1
```

# Documentation

Pay attention, the documentation is not up to date due to several changes.

* [Command line](docs/commandline.md)
* [Distributors](docs/distributor.md)
* [Task-Sets](docs/taskset.md)
* [Tasks](docs/tasks.md)
* [Mixins](docs/mixins.md)
* [Optimization](docs/optimization.md)
* [Live Request Handler](docs/live.md)
* [Dictionary to XML format](docs/dict2xml.md)


# ToDo List

[ ] Makefile Integration
    [ ] new task build directory (`taskgen/bin`)
    [ ] taskgen requirements
[ ] Refactor Distributor (move ping functionality to Session)
[ ] Update Documentation
[ ] Replace Live & Profile Requests by **Th3 Aw3soMe Push**

# Branches
* `taskgen` supports the current live request functionality.
* `push` replaces live/profile requests by push logging.

