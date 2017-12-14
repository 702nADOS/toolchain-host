from taskgen.event import AbstractEventHandler


class SqliteLogger(AbstractEventHandler):

    def __init__(self):
        self._logger = logging.getLogger("SqliteLogger")
    
    def __taskset_event__(self, taskset, log_xml):
        try:
            log_dict = xmltodict.parse(log_xml)
        except:
            self._logger.critical("unable to parse log data.")

    def __taskset_start__(self, taskset):
        pass

    def __taskset_finish__(self, taskset):
        pass

    def __taskset_stop__(self, taskset):
        pass




