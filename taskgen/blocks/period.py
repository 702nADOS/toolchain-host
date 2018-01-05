import random

def Custom(period):
    return {
        "period" : period
    }

def Variants():
    return Custom(range(20))

def Random():
    return Custom(random.randint(1, 20))

def HighRandom():
    return Custom(random.randint(1, 5))

def MediumRandom():
    return Custom(random.randint(5, 10))

def LowRandom():
    return Custom(random.randint(10, 20))

