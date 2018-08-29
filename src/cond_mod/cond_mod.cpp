#include <base/printf.h>
#include <base/component.h>

void Component::construct(Genode::Env &env)
{
	unsigned int n=1000;

	/*const Genode::Xml_node& config_node = Genode::config()->xml_node();
	config_node.sub_node("arg1").value<unsigned int>(&n);*/

	if(n%2==0){
		PINF("Finished!");

		env.parent().exit(0);
	}

	for(unsigned int i=0;i<n;i++){
		asm("nop");
	}

	env.parent().exit(0);
}
