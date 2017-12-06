`taskgen` is the command line tool for distributing and running task-sets at
multiple destination instances.

# Show help information
```
./taskgen --help
./taskgen run --help
./taskgen list --help
```

# Connect to a range of IP addresses

IP ranges are defined as
[CIDR](https://de.wikipedia.org/wiki/Classless_Inter-Domain_Routing)
format. Before a connection is established, all host are pinged.

```
./taskgen run -t example.ExampleTaskSet -p 1234 172.25.0.0/24
```

# Connect to multiple IP addresses or IP ranges

```
./taskgen run -t example.ExampleTaskSet -p 1234 172.25.0.0/24 172.26.0.0/24
```

# Write log to file

```
./taskgen run --log-file log.txt -t example.ExampleTaskSet -p 1234 172.25.0.1
```

# Increase verbosity

```
./taskgen run -vvv -t example.ExampleTaskSet -p 1234 172.25.0.1
```

# Pretend the connection

When the `--pretend` option is used, no real connection is established and the
SimpleDistributor is replaced with the LogDistributor. The actual sent xml files
are printed to stdout.

```
./taskgen run --pretend -t example.ExampleTaskSet -p 1234 172.25.0.1
```

# Choose a Live Request Handler

```
./taskgen run -l sqlite.SQLiteLiveHandler -p 1234 172.25.0.1
```

# Choose an optimization

```
./taskgen run -o fairness.Fairness -p 1234 172.25.0.1
```

# List all available task-sets

```
./taskgen list -t
```

# List all available optimizations

```
./taskgen list -o
```

# List all available live request handlers

```
./taskgen list -l
```

