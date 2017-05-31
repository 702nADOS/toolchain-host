#!/bin/bash

for i in {0..100}
 do
   cp log_task_v1.xml log_task$i.xml
   period=$((42+$i*100)) 
   echo $period
   sed -i -e 's/changehere/'$period'/g' log_task$i.xml
done




