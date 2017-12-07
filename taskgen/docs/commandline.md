`taskgen` is the command line tool for distributing and running task-sets at
multiple destination instances.

```bash
$ ./taskgen run --help
usage: taskgen run [-h] [-v] [--log-file FILE] -p PORT -t CLASS [-l CLASS]
                   [-o CLASS] [--pretend]
                   IP [IP ...]
```

| Command | Parameter          | Description                                |
| ------- | ------------------ | ------------------------------------------ |
| list    | -h, --help         | show this help message                     |
| list    | -t, --taskset      | print all available taskset  classes       |
| list    | -o, --optimization | print all available optimization classses  |
| list    | -l, --live         | print all available live request handler   |

| Command | Parameter                      | Description                                         |
| ------- | ------------------------------ | --------------------------------------------------- |
| run     | -h, --help                     | show this help message                              |
| run     | -v, --verbosity                | increase output verbosity                           |
| run     | --log-file FILE                | write log to file                                   |
| run     | -p PORT, --port PORT           | destination port                                    |
| run     | -t CLASS, --taskset CLASS      | select a taskset class                              |
| run     | -o CLASS, --optimization CLASS | select an optimization class                        |
| run     | -l CLASS, --live CLASS         | select a live request handler                       |
| run     | --pretend                      | pretend to send the taskset                         |
| run     | IP [IP ...]                    | IP address or a range of IP addresses (CIDR format) |


# Examples

Send the example taskset to all hosts in `172.25.0.0/24`. Before a connection is
established, all host are pinged. IP ranges are defined as
[CIDR](https://de.wikipedia.org/wiki/Classless_Inter-Domain_Routing)
format. 

```bash
./taskgen run -t example.ExampleTaskSet -p 1234 172.25.0.0/24
```

Connect to multiple IP addresses or IP ranges:

```bash
./taskgen run -t example.ExampleTaskSet -p 1234 172.25.0.0/24 172.26.0.0/24
```

Write log to file:

```bash
./taskgen run --log-file log.txt -t example.ExampleTaskSet -p 1234 172.25.0.1
```

Increase verbosity:

```bash
./taskgen run -vvv -t example.ExampleTaskSet -p 1234 172.25.0.1
```

Pretend the connection:

When the `--pretend` option is used, no real connection is established and the
SimpleDistributor is replaced with the LogDistributor. The actual sent xml files
are printed to stdout.

```bash
./taskgen run --pretend -t example.ExampleTaskSet -p 1234 172.25.0.1
```

Choose a Live Request Handler:

```bash
./taskgen run -l sqlite.SQLiteLiveHandler -p 1234 172.25.0.1
```

Choose an optimization:

```bash
./taskgen run -o fairness.Fairness -p 1234 172.25.0.1
```

List all available task-sets:

```bash
./taskgen list -t
```

List all available optimizations:

```bash
./taskgen list -o
```

List all available live request handlers:

```bash
./taskgen list -l
```

