class MixinMeta(type):

    def __new__(cls, name, bases, attrs):
        new_class = super(MixinMeta, cls).__new__(cls, name, bases, attrs)

        # update _task scheme by Base classes
        base_tasks = [bc._task for bc in bases if hasattr(bc, '_task')]
        tasks = [new_class._task] + base_tasks

        new_class._task = {}
        for task in tasks:
            new_class._task.update(task)

        return new_class


class Mixin(object, metaclass = MixinMeta):
    _task = {}
    pass
