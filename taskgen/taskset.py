import xmltodict
import os

from pprint import pprint as pp


class TaskSet:
    def __init__(self, taskset = None):
        self._taskset = taskset

    @staticmethod
    def writeall(tasksets, path, prefix="taskset_"):
        for index, taskset in enumerate(tasksets):
            taskset.write(path + "/" + prefix + "_" + str(index) + ".xml")

    @staticmethod
    def readall(path):
        for filename in os.listdir(path):
            if filename.endswith(".xml"):
                path = os.path.join(path, filename)
                yield open(path,'rb').read()

    def dump(self):
        return xmltodict.unparse(self._taskset, pretty=True)

    def write(self, path):
        with open(path, 'a') as out:
            out.write(self.dump())

    def read(self, path):
        xml = open(path,'rb').read()
        self._taskset = xmltodict.parse(xml)


    
