#include <iostream>
#include <base/printf.h>
#include <util/xml_node.h>
#include <base/attached_rom_dataspace.h>
#include <libc/component.h>

int main()
{
		Genode::log("cond_42 hello!");	
	
		unsigned int n=1000;

		/*Genode::Attached_rom_dataspace config(_env, "config");
		const Genode::Xml_node& config_node = config.xml().sub_node("arg1");
		config_node.value<unsigned int>(&n);*/

		if(n==42){
			Genode::log("Can not count because 42!");

			return 0;
		}

		unsigned int counter=0;

		Genode::log("counting!");

		for(unsigned int i=0;i<n;i++){
			counter+=1;
		}


		Genode::log("Counted ", counter);

		return 0;
}

void Libc::Component::construct(Libc::Env&)
{
	Libc::with_libc([&] () {exit(main());});
}
