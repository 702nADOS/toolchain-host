#include <iostream>
#include <base/printf.h>
#include <libc/component.h>

int main(void)
{
	PINF("hey: Hello!\n");
	return 0;
}

void Libc::Component::construct(Libc::Env&)
{
	Libc::with_libc([&] () {exit(main());});
}
