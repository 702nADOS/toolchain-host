#!/bin/bash

name=pi
crit_time=2000
quota=5M

for i in {0..99}
 do
	cp change_me_task.xml $name$i.xml
	arg=$((100+$i*$i*500)) 
   
	sed -i -e 's/changeme_arg/'$arg'/g' -e 's/changeme_quota/'$quota'/g' -e 's/changeme_id/'$i'/g' -e 's/changeme_crit/'$crit_time'/g' -e 's/changeme_bin/'$name'/g' $name$i.xml
done


