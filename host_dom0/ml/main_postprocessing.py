import random
import time
import os.path, sys
from tools.db import db
from tools.task import task
import xml.etree.ElementTree



folder = "../toolchain-host/host_dom0/"
filename = "log_profile"

binary_name = "02.pi"


file_counter=0

while os.path.isfile(folder+filename+str(file_counter)+".xml"):
    file=folder+filename+str(file_counter)+".xml"
    print "Processing file"+file
    
    xml_root = xml.etree.ElementTree.parse(file).getroot()
    
    
    task_list = xml_root.find('task-descriptions')
    
    for task in task_list:
        att_list = task.attrib
        if binary_name in att_list['thread']: 
            if "1" in att_list['state']:
                print "Task: "+binary_name+" arrival_time: "+str(att_list['arrival-time'])+" execution_time: "+str(att_list['execution-time'])+" state: "+str(att_list['state'])
            
      
    print "\n"  
    
    file_counter+=1
    
    
    
    
    

#Deadline reached auf positiv setzen
#werte durchgehen
#    Waehrend deadline reached positiv 
#        berechne fuer aktuellen task ob erfolgreiche ausfuehrung
#        falls nicht deadline negativ setzen
#
#Spass mit der DB
