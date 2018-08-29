#include <base/printf.h>
#include <base/component.h>

void Component::construct(Genode::Env &env)
{
	PINF("idle: Hello!\n");

	while (true);

	env.parent().exit(0);
}
