`taskgen` is the command line tool for distributing and running task-sets at
multiple destination instances.

```bash
$ ./taskgen run --help
usage: taskgen run [-h] [-d] [-p PORT] -t CLASS [CLASS ...] [-e CLASS]
                   [-o CLASS] [-s CLASS]
                   IP [IP ...]

positional arguments:
  IP                    IP address or a range of IP addresses (CIDR format)

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Print debugging information.
  -p PORT, --port PORT  Port, default is port number 3001.
  -t CLASS [CLASS ...], --taskset CLASS [CLASS ...]
                        Select a taskset class.
  -e CLASS, --event CLASS
                        Select a event handler for incoming events of
                        processed tasksets.
  -o CLASS, --optimization CLASS
                        Select an optimization class.
  -s CLASS, --session CLASS
                        Select a session class. Default: GenodeSession
```

| Command | Parameter          | Description                                |
| ------- | ------------------ | ------------------------------------------ |
| list    | -h, --help         | show this help message                     |
| list    | -t, --taskset      | print all available taskset  classes       |
| list    | -o, --optimization | print all available optimization classses  |
| list    | -e, --event        | print all available event handler          |
| list    | -s, --session      | print all available session classes        |

| Command | Parameter                      | Description                                         |
| ------- | ------------------------------ | --------------------------------------------------- |
| run     | -h, --help                     | show this help message                              |
| run     | -d, --debug                    | print debug information to stdout                   |
| run     | -p PORT, --port PORT           | destination port. default: 3001                     |
| run     | -t CLASS, --taskset CLASS      | select a taskset class                              |
| run     | -o CLASS, --optimization CLASS | select an optimization class                        |
| run     | -e CLASS, --event CLASS        | select a event handler class                        |
| run     | -s CLASS, --session CLASS      | select a session class. default: PingSession        |
| run     | IP [IP ...]                    | IP address or a range of IP addresses (CIDR format) |


# Examples

Send the example taskset to all hosts in `172.25.0.0/24`. Before a connection is
established, all host are pinged. IP ranges are defined as
[CIDR](https://de.wikipedia.org/wiki/Classless_Inter-Domain_Routing)
format. 

```bash
./taskgen run -t example.Hey0TaskSet 172.25.0.0/24
```

Connect to multiple IP addresses or IP ranges:

```bash
./taskgen run -t example.Hey0TaskSet 172.25.0.0/24 172.26.0.0/24
```

Enable debug information:

```bash
./taskgen run -d -t example.Hey0TaskSet 172.25.0.1
```

Pretend the connection with `StdIOSession`:

When using the `stdio.StdIOSession` session, no real connection is established
and the actual task-sets are printed to stdout.

```bash
./taskgen run  -t example.Hey0TaskSet -s stdio.StdIOSession 172.25.0.1
```

Event Handlers handle incoming event logs:
```bash
./taskgen run -e sqlite.SQLiteLiveHandler 172.25.0.1
```

Choose an optimization:

```bash
./taskgen run -o fairness.Fairness 172.25.0.1
```

List all available task-sets:

```bash
./taskgen list --taskset
```

List all available optimizations:

```bash
./taskgen list --optimization
```

List all available event handlers:

```bash
./taskgen list --event
```

List all available sessions:

```bash
./taskgen list --session
```

