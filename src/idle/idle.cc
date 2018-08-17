#include <iostream>
#include <base/printf.h>
#include <libc/component.h>

int main(void)
{
	PINF("idle: Hello!\n");

	while (true);

	return 0;
}

void Libc::Component::construct(Libc::Env&)
{
	Libc::with_libc([&] () {exit(main());});
}
