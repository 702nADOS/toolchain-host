#!/bin/bash

name=hey
crit_time=80
quota=5M

name2=pi
crit_time2=2000
quota2=5M

for i in {0..99}
 do
	cp change_me_task.xml ${name}_${name2}${i}.xml
	arg=0
   	crit_time=$(($crit_time+$i*5))

	arg2=$((100+$i*$i*500))
	
	sed -i -e 's/changeme_arg1/'$arg'/g' -e 's/changeme_quota1/'$quota'/g' -e 's/changeme_id1/'$i'/g' -e 's/changeme_crit1/'$crit_time'/g' -e 's/changeme_bin1/'$name'/g' -e 's/changeme_arg2/'${arg2}'/g' -e 's/changeme_quota2/'${quota2}'/g' -e 's/changeme_id2/'$i'/g' -e 's/changeme_crit2/'${crit_time2}'/g' -e 's/changeme_bin2/'${name2}'/g' ${name}_${name2}${i}.xml





done


