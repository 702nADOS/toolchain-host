#include <iostream>
#include <base/printf.h>
#include <libc/component.h>

int main(){
	unsigned int n=1000;

	/*const Genode::Xml_node& config_node = Genode::config()->xml_node();
	config_node.sub_node("arg1").value<unsigned int>(&n);*/

	if(n%2==0){
		PINF("Finished!");

		return 0;
	}

	for(unsigned int i=0;i<n;i++){
		asm("nop");
	}



	return 0;
}

void Libc::Component::construct(Libc::Env&)
{
	Libc::with_libc([&] () {exit(main());});
}
