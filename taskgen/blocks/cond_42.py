import random


"""
Fulfills the condition, which terminates the program without counting.
`cond_42` immediately, if `args1` is 42
"""
def Custom(arg1):
    return {
        "pkg" : "cond_mod",
        "quota" : "1M",
        "config" : {
            "arg1" : arg1
        }
    }


"""
Terminates immediately the program.
"""
def Break():
    return Custom(42)


"""
Random argument `arg1`, `n` is the maximum value for `arg1`.
"""
def Random(n):
    return Custom(random.randint(1, n))


"""
Creates variants of looping.
"""
def Variants(variants):
    return Custom(range(variants))
