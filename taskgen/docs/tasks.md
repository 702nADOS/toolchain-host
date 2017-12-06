# Xml mapping

When it comes to the transmission of a task-set to a genode instance, a `Task`
is translated to a xml representation. All dictionary attributes, even nested
dictionaries, are directly mapped to a xml element. Adding and altering
attributes can be done by using the `dict` methods of the `Task` object or
implementing a `Mixin`. The actual conversation is done by the
[xmltodict](https://github.com/martinblech/xmltodict) library.

# Variants

Every attribute in the Task can be a single value or of type `Iterable`. It is
possible to define ranges (`rang(0,10)`), lists (`[0,1,2,3]`) or custom
[generators](https://wiki.python.org/moin/Generators). Multiple options for a
value results in multiple variants of a task and finally in various tasksets.
Each variant of taskset is finally processed by one genode instance.


