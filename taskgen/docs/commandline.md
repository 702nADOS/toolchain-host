`taskgen` is the command line tool for distributing and running task-sets at
multiple destination instances.

```bash
./taskgen --help
./taskgen run --help
./taskgen list --help
```

# Connect to a range of IP addresses

IP ranges are defined as
[CIDR](https://de.wikipedia.org/wiki/Classless_Inter-Domain_Routing)
format. Before a connection is established, all host are pinged.

```bash
./taskgen run -t example.ExampleTaskSet -p 1234 172.25.0.0/24
```

# Connect to multiple IP addresses or IP ranges

```bash
./taskgen run -t example.ExampleTaskSet -p 1234 172.25.0.0/24 172.26.0.0/24
```

# Write log to file

```bash
./taskgen run --log-file log.txt -t example.ExampleTaskSet -p 1234 172.25.0.1
```

# Increase verbosity

```bash
./taskgen run -vvv -t example.ExampleTaskSet -p 1234 172.25.0.1
```

# Pretend the connection

When the `--pretend` option is used, no real connection is established and the
SimpleDistributor is replaced with the LogDistributor. The actual sent xml files
are printed to stdout.

```bash
./taskgen run --pretend -t example.ExampleTaskSet -p 1234 172.25.0.1
```

# Choose a Live Request Handler

```bash
./taskgen run -l sqlite.SQLiteLiveHandler -p 1234 172.25.0.1
```

# Choose an optimization

```bash
./taskgen run -o fairness.Fairness -p 1234 172.25.0.1
```

# List all available task-sets

```bash
./taskgen list -t
```

# List all available optimizations

```bash
./taskgen list -o
```

# List all available live request handlers

```bash
./taskgen list -l
```

