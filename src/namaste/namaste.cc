#include <base/printf.h>
#include <base/component.h>

void Component::construct(Genode::Env &env)
{
	Genode::log("namaste: Hello!");
	env.parent().exit(0);
}
