# Events & Event Handlers

Whenever a task starts or terminates an event is sent. These events are handled
over to an event handler. Furthermore, an event handler decides if a task-set
processing continues or should stop. 

| Event Handler Class | Description |
| --- | --- |
| event.AbstractEventHandler | If you want to handle the task-set continue-logic by yourself, this might be the starting point. |
| event.DefaultEventHandler | Updates tasks with incoming event data and stop task-set processing if all tasks are terminated. |
| events.sql.SqliteHandler | Stores incoming events to a sqlite database. |
| events.csv.CsvHandler | Stores incoming events to a csv file. |

```python3
from taskgen.distributor import Distributor
from taskgen.sql import SqliteHandler

distributor = Distributor("172.25.1.2")

# create event handler
event_handler = SqliteHandler("events.db")

# handle over it
distributor.event_handler = event_handler
```

# Events

An event has the xml format:

```XML
<profile>
	<events>
		<event type="START" task-id="0" time-stamp="276427"/>
		<event type="EXIT" task-id="0" time-stamp="277087"/>
	</events>
</profile>
```

Which is translated with [xmltodict](xmltodict.md) to a dictionary object.

```Python3
{
    "profile": {
        "events": {
            "event": [ 
                {"@type": "START", "@task-id": "0", "@time-stamp": "276427"}, 
                {"@type": "EXIT", "@task-id": "0", "@time-stamp": "277087"}
            ]
        }
    }
}
```


# Implementation

If you want to extend taskgen with another event handler,
`event.DefaultEventHandler` is the way to go.  It is important, that
`__taskset_event__` returns a boolean. `True` if the task-set is still running,
`False` if the taskset is finished, or if you want to cancel the current
task-set processing. In general, `DefaultEventHandler` already keeps track of it
and you only need to pass through the value inside `__taskset_event__`.


```Python3
from taskgen.event import DefaultEventHandler

class YourHandler(DefaultEventHandler):

    def __init__(self):
        super().__init__()
        # YOUR implementation
        
    def __taskset_event__(self, taskset, event):
        running = super().__taskset_event__(taskset, event)

        # YOUR implementation
        
        return running
    
    def __taskset_start__(self, taskset):
        # YOUR implementation
        pass

    def __taskset_finish__(self, taskset):
        # YOUR implementation
        pass

    def __taskset_stop__(self, taskset):
        # YOUR implementation
        pass
```
