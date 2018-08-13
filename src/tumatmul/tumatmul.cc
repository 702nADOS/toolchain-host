#include <list>
#include <cmath>
#include <algorithm>
#include <string>
#include <base/printf.h>
#include <libc/component.h>

int main(void)
{
	Genode::log("tumatmul: Hello!");

	// Sieve of Erathosthenes
	unsigned int max = 0;
	/*const Genode::Xml_node& config_node = Genode::config()->xml_node();
	config_node.sub_node("arg1").value<unsigned int>(&max);*/
	unsigned int sqrt = static_cast<unsigned int>(std::sqrt(max));

	Genode::log("Calculating primes up to ", max);
	std::list<unsigned int> primes;
	for (unsigned int i = 2; i <= max; ++i)
	{
		primes.push_back(i);
	}

	for (auto tester = primes.cbegin(); *tester <= sqrt; ++tester)
	{
		auto testee = tester;
		++testee;
		for (; testee != primes.cend(); ++testee)
		{
			if (*testee % *tester == 0)
			{
				primes.erase(testee);
			}
		}
	}

	std::string primes_str;

	auto it = primes.crbegin();
	for (size_t i = 0; i <= 5 && it != primes.crend(); ++i, ++it)
	{
		primes_str += std::to_string(*it) + ' ';
	}
	Genode::log("Last 5 primes up to ", max, primes_str.c_str());
	Genode::log("Calculated primes in total ", primes.size());

	return 0;
}

void Libc::Component::construct(Libc::Env&)
{

}
