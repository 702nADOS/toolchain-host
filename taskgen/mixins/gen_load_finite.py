from .mixin import Mixin
# THIS is not the way, how class should be defined. Generally, you use an
# additional .py file. But we abuse it as configuration file.

class GenLoadFiniteBlob(Mixin):
    _task = {
        "pkg" : "gen_load_finite",
        "quota" : "1M",
        "config" : {
            "arg1" : 126546,
            "arg2" : range(0, 10)
            
        }
    }

    def __str__(self):
         return "Finite load"
