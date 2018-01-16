import random

def Custom(number):
    return {
        "numberofjobs" : number,
    }

"""
Random the number of jobs, Maxium of jobs is 20.
"""
def Random():
    return Custom(random.randint(1, 20))


def Variants():
    return Custom(range(20))
