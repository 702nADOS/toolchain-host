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

name4=hey
crit_time4=70
quota4=5M

name5=cond_mod
crit_time5=100
quota5=5M

name6=cond_42
crit_time6=100
quota6=5M


for i in {0..99}
 do
	cp change_me_task.xml ${name}_${name2}_${name3}_${name4}_${name5}_${name6}${i}.xml
	arg=$((1000+$i*10000))
   	#crit_time=$(($crit_time+$i*5))

	arg2=$((100+$i*$i*500))

	arg3=$(($i*5))

	crit_time4=$(($crit_time+$i*5))
	arg4=0

	arg5=$(($i*1001))
	
	arg6=$(($i*2))
	sed -i -e 's/changeme_arg1/'$arg'/g' -e 's/changeme_quota1/'$quota'/g' -e 's/changeme_id1/'$i'/g' -e 's/changeme_crit1/'$crit_time'/g' -e 's/changeme_bin1/'$name'/g' -e 's/changeme_arg2/'${arg2}'/g' -e 's/changeme_quota2/'${quota2}'/g' -e 's/changeme_id2/'$i'/g' -e 's/changeme_crit2/'${crit_time2}'/g' -e 's/changeme_bin2/'${name2}'/g' -e 's/changeme_arg3/'${arg3}'/g' -e 's/changeme_quota3/'${quota3}'/g' -e 's/changeme_id3/'$i'/g' -e 's/changeme_crit3/'${crit_time3}'/g' -e 's/changeme_bin3/'${name3}'/g' -e 's/changeme_arg4/'${arg4}'/g' -e 's/changeme_quota4/'${quota4}'/g' -e 's/changeme_id4/'$i'/g' -e 's/changeme_crit4/'${crit_time4}'/g' -e 's/changeme_bin4/'${name4}'/g'   -e 's/changeme_arg5/'${arg5}'/g' -e 's/changeme_quota5/'${quota5}'/g' -e 's/changeme_id5/'$i'/g' -e 's/changeme_crit5/'${crit_time5}'/g' -e 's/changeme_bin5/'${name5}'/g'   -e 's/changeme_arg6/'${arg6}'/g' -e 's/changeme_quota6/'${quota6}'/g' -e 's/changeme_id6/'$i'/g' -e 's/changeme_crit6/'${crit_time6}'/g' -e 's/changeme_bin6/'${name6}'/g' ${name}_${name2}_${name3}_${name4}_${name5}_${name6}${i}.xml





done


