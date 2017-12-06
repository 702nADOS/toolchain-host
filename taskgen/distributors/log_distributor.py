import logging

from taskgen.live import LiveResult
from taskgen.taskset import TaskSet
from taskgen.distributor import AbstractDistributor

# stub
import time
    
class LogDistributor(AbstractDistributor):
    
    def __init__(self, host, port):
        self.logger = logging.getLogger("LogDistributor")
        self.logger.debug("stub created")

    def start(self, optimization, taskset):
        self.logger.debug("start of taskset")
        self._timestamp = time.clock()

    def stop(self):
        self.logger.debug("stop of taskset")

    def live_request(self):
        return LiveResult({
            'running' : time.clock() - self._timestamp < 0.1 # 5 seconds
        })

    def close(self):
        self.logger.debug("connection closed")

