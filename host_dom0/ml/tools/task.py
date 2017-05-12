import os
import time


class task:
    name = ""
    arrival_time = 0
    finishing_time = 0
    deadline_reached = True
    execution_time = 0
    state = -1
    
    def __init__(self, name, arrival_time, finishing_time, deadline_reached, execution_time, state):
       self.name = name
       self.arrival_time = arrival_time
       self.finishing_time = finishing_time
       self.deadline_reached = deadline_reached
       self.execution_time = execution_time
       self.state = state
                
    def output(self, msg):
        for line in msg.splitlines():
            print "Task("+name+"): " + line
        
   