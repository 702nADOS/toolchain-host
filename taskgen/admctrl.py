import xmltodict

class AdmCtrl(dict):
    def asxml(self):
        return xmltodict.unparse(self, pretty=True)
