#include <iostream>
#include <iomanip>
#include <cmath>
#include <base/printf.h>
#include <sstream>
#include <libc/component.h>
#include <base/child.h>
#include <base/attached_rom_dataspace.h>

using namespace std;

/*
 * Using the Gregory-Leibniz series to calculate pi
 * https://de.wikipedia.org/wiki/Leibniz-Reihe
 */

void Libc::Component::construct(Libc::Env &env)
{
	Libc::with_libc([&] () {
		unsigned int n=50;

		Genode::Attached_rom_dataspace config(env, "config");
		const Genode::Xml_node& config_node = config.xml().sub_node("arg1");
		config_node.value<unsigned int>(&n);
		PINF("Calculating pi(e) using e=%d iterations in an inefficient way.",n);


		double y=0.0;



		for(unsigned int i=0;i<n;i++){
			int iter_signed = ((i%2)*-2)+1;

			y += iter_signed/(2.0*i+1);
		}

		double pi = y*4;
		std::stringstream ss;
		ss << fixed << setprecision( 15 ) << pi;

		PINF("Using %d iterations pi should be ~ %s",n, ss.str().c_str());


		env.parent().exit(0);
	});
}
