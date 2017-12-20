"""
Using the Gregory-Leibniz series to calculate pi
[Leibniz-Reihe]( https://de.wikipedia.org/wiki/Leibniz-Reihe)
"""
import random


def Custom(arg1):
    return {
        "pkg" : "pi",
        "quota" : "1M",
        "config" : {
            "arg1" : arg1
        }
    }


"""
Random argument `arg1`, `n` is the maximum value for `arg1`.
"""
def Random(n):
    return Custom(random.randint(1, n))



def Variants(variants):
    return Custom(range(variants))
