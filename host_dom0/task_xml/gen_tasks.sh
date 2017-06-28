#!/bin/bash

for i in {0..100}
 do
   cp change_me_task.xml log_task$i.xml
   value1=$((42+$i*100)) 
   value2=5M
   sed -i -e 's/changeme1/'$value1'/g' -e 's/changeme2/'$value2'/g' log_task$i.xml
done




