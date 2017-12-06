TODO explain distributors

# LogDistributor

The `LogDistributor` is a stub implementation for the low level communication
with a genode instance. Combined with the `MultiDistributor`, it helps you
debugging. Instead of sending all task-sets, the xml representation is printed
to stdout.

# SimpleDistributor

The `SimpleDistributor` represents the most simple implementation of a
distributor. It connects to one genode instance and processes one taskset. It is
able to start, stop, close and send live requests. Please do not use this
distributor directly, it only abstracts the low level communication for the more
advanced `MultiDistributor`.

# MultiDistributor

The `MultiDistributor` is the default distributor for communication with
multiple genode instances.

* IP ranges
* ping
* asyncron
* push back, no reconnect
* example



