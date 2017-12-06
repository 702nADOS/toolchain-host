import xmltodict

class Optimization(dict):
    def asxml(self):
        return xmltodict.unparse(self, pretty=True)
