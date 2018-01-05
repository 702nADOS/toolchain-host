import random

# kernel: 256 priorties
    # genode: 128 priorities
def Custom(priority):
    return {            
        "priority" : priority
    }

def Variants():
    return Custom(range(1, 128))

def Random():
    return Custom(random.randint(1, 128))

def HighRandom():
    return Custom(random.randint(1, 42))

def MediumRandom():
    return Custom(random.randint(42, 84))

def LowRandom():
    return Custom(random.randint(84, 128))



        
