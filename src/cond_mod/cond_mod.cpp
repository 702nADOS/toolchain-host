#include <base/printf.h>
#include <base/component.h>
#include <base/attached_rom_dataspace.h>

void Component::construct(Genode::Env &env)
{
	unsigned int n=1000;

	Genode::Attached_rom_dataspace config(env, "config");
	const Genode::Xml_node& config_node = config.xml().sub_node("arg1");
	config_node.value<unsigned int>(&n);

	if(n%2==0){
		PINF("Finished!");

		env.parent().exit(0);
	}

	for(unsigned int i=0;i<n;i++){
		asm("nop");
	}

	env.parent().exit(0);
}
