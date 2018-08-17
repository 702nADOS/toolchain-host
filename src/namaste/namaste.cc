#include <iostream>
#include <base/printf.h>
#include <libc/component.h>

int main(void)
{
	PINF("namaste: Hello!\n");
}

void Libc::Component::construct(Libc::Env&)
{
	Libc::with_libc([&] () {exit(main());});
}
