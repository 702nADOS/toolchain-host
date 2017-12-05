from .mixin import Mixin

class GenLoadFiniteBlob(Mixin):
    _task = {
        "pkg" : "gen_load_finite",
        "quota" : "1M",
        "config" : {
            "arg1" : 126546,
            "arg2" : 1
            
        }
    }

    def __str__(self):
         return "Finite load"
