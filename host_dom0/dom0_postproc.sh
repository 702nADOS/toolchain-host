#!/bin/bash


cat dom0_output.log | grep "exited with exit value 0"  > tmp_success_tasks.log 

while read -r line
do
	read -a arr<<<$line
	echo ${arr[7]} >> suc_tasks.log
done < tmp_success_tasks.log




rm tmp_success_tasks.log

