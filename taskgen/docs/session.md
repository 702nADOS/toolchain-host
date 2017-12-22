# Sessions

The low level communication between the `Distributor` and a target system is
done by a Session class.

| Session Class | Description |
| --- | --- |
| `session.AbstractSession` | Abstract class for a session. Use this for implementing new sessions |
| `sessions.genode.GenodeSession` | Basic communication with `genode-Taskloader`. |
| `sessions.genode.PingSession` | Extends the `GenodeSession` by a ping check before a connection is established |
| `sessions.stdio.StdIOSession` | Prints task-sets to stdout instead of sending it **DEBUGGING** |

# Implementation

A Session needs to inherit from `session.AbstractSession` and implement the
static method `is_available` and abstract methods `start`, `stop`, `event`,
`close`. `is_available` is called before the class is initialized and checks if
the host is available. For example `PingSession` implements this method and does
a simple ping test. Read the pydocs of `session.py` for more information,
please.
