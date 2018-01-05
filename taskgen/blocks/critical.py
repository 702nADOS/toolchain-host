def Custom(criticality):
    return {            
        "critical-time" : criticality
        }
        
High = Custom( range(1,5))

Medium = Custom( range(5,10))

Low = Custom( range(10,15))

