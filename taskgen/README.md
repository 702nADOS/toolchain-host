# taskgen

A taskset generation framework for the
[genode-Taskloader](https://github.com/argos-research/genode-Taskloader)
component.


# Status

* All components are implemented and work. 
* Tasks with multiple jobs are not handled well [issue](https://github.com/argos-research/genode-Taskloader/issues/5).

# Todos

## Version 0.9 *current*

## Version 1.0 *stable API*

- [x] Rename `EventHandler` to `Monitor` *reason: more common and less chars*
- [x] Rename `Attribute` to `Task-Block` *reason: no meaning conflicts*
- [x] Rename `Optimization` to `AdmCtrl` *reason: advisors' decision*
- [x] Add optional passthrough of attributes to Sessions and Distributor
  *pending next meeting*
- [ ] Solve
  [issue](https://github.com/argos-research/genode-Taskloader/issues/5).
- [ ] Add simpler task-set, which works with current implementation of
  `genode-Taskloader`.
- [ ] pydocs
  - [ ] Distributor
  - [ ] AbstractSession
  - [ ] AbstractMonitor
- [x] Update Documentation
- [x] Move xml parsing to Sessions

## Version 1.1

- [ ] Replace `Thread` implementation with python's multi processing.

## Version 1.2

- [ ] Implementation of [SqliteEventHandler](events/sqlite.py)
- [ ] Implementation of [CsvEventHandler](events/csv.py)
- [ ] Implementation of [StdIOSession](sessions.stdio.py)
- [ ] Implementation of [FileSession](sessions.file.py)

## Version 1.3


- [ ] Machine Learning Show Case
- [ ] Benchmarks

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
  
- **User friendly** Threading keeps waiting time low and work, like ping,
  connect, processing tasksets, is done in background. A fast-responsive
  framework is the result.


# Installation

```
pip3 install --user -r ./requirements.txt
```

taskgen only works with:

* [push_profile](https://github.com/argos-research/genode-Taskloader/tree/push_profile) branch of genode-Taskloader
* [networker_thread](https://github.com/argos-research/genode-dom0-HW/tree/networker_thread) branch of genode-dom0-HW

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

Task-sets in `example.*` are good starting points for testing and exploring
taskgen.

We want to distribute the `example.Hey0TaskSet` task-set to one destination
instance. The `stdio.StdIOSession` session prints the task-set to stdout,
instead of sending it over the network. 

```bash
./taskgen run -d -t example.Hey0TaskSet -s stdio.StdIOSession 172.25.0.1
```

# Documentation
* [Overview](docs/overview.md) **up-to-date**
* [Command line](docs/commandline.md) **up-to-date**
* [Distributors](docs/distributor.md) **up-to-date**
* [Task-Sets](docs/taskset.md) **up-to-date**
* [Tasks](docs/tasks.md) **up-to-date**
* [Task Blocks](docs/blocks.md) **up-to-date**
* [Admission Control](docs/admctrl.md) **up-to-date**
* [Monitors](docs/monitor.md) **up-to-date**
* [Sessions](docs/session.md) **up-to-date**
* [Dictionary to XML format](docs/dict2xml.md) **up-to-date**

