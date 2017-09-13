#!/bin/bash

name=tumatmul
crit_time=1000
quota=5M

name2=pi
crit_time2=2000
quota2=5M

name3=linpack
crit_time3=2000
quota3=5M

for i in {0..99}
 do
	cp change_me_task.xml ${name}_${name2}_${name3}${i}.xml
	arg=$((1000+$i*10000))
   	#crit_time=$(($crit_time+$i*5))

	arg2=$((100+$i*$i*500))

	arg3=$(($i*5))
	
	sed -i -e 's/changeme_arg1/'$arg'/g' -e 's/changeme_quota1/'$quota'/g' -e 's/changeme_id1/'$i'/g' -e 's/changeme_crit1/'$crit_time'/g' -e 's/changeme_bin1/'$name'/g' -e 's/changeme_arg2/'${arg2}'/g' -e 's/changeme_quota2/'${quota2}'/g' -e 's/changeme_id2/'$i'/g' -e 's/changeme_crit2/'${crit_time2}'/g' -e 's/changeme_bin2/'${name2}'/g' -e 's/changeme_arg3/'${arg3}'/g' -e 's/changeme_quota3/'${quota3}'/g' -e 's/changeme_id3/'$i'/g' -e 's/changeme_crit3/'${crit_time3}'/g' -e 's/changeme_bin3/'${name3}'/g' ${name}_${name2}_${name3}${i}.xml





done


