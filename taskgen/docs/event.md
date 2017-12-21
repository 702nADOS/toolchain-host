# Live Request Handlers

All data from a genode instance are pulled with *live* requests. The result of a
*live* request is represented with the `LiveResult` class. Live Request Handlers
handle `LiveResult`s and for example stores them to sqlite databases. Live
Handlers implementations are in the [lives](../lives) directory.

```python3
from taskgen.lives.sqlite import SQLiteLiveHandler
from taskgen.tasksets.example import ExampleTaskSet
from taskgen.distributors.multi_distributor import MultiDistributor

md = MultiDistributor("172.25.0.1", 1234)

# save all live requests to a sqlite db.
md.live_handler = SQLiteLiveHandler("./live.db")

ts = ExampleTaskSet()
md.start(ts, opt)
```
