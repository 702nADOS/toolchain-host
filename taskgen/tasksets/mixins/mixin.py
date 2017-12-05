class MixinMeta(type):

    def __new__(cls, name, bases, attrs):
        new_class = super(MixinMeta, cls).__new__(cls, name, bases, attrs)
#        for bc in bases:
            #new_class.update(bc)

        return new_class


class Mixin(dict, metaclass = MixinMeta):
    pass
