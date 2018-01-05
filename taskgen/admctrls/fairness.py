from taskgen.admctrl import AdmCtrlData

# TO NOT CHANGE, used in documentation
class Fairness(AdmCtrlData):
    """ Fairness Optimization class exmaple"""
    def __init__(self):
        super().__init({
            "optimize" : {
                "goal" : {
                    "fairness" : {
                        "apply" : 1
                    },
                    "utilization" : {
                        "apply" : 0
                    }
                },
                "query_interval" : 1000
            }
        })
        
