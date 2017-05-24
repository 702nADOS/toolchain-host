import random
import time
import os.path, sys
from tools.db import db
from tools.task import task
import xml.etree.ElementTree
from tools.machine_learning.SGD import SGD
from tools.machine_learning.SVC_dummy import SVC_dummy
from tools.machine_learning.SVC_linear import SVC_linear
from tools.machine_learning.SVC_poly import SVC_poly
from tools.machine_learning.SVC_rbf import SVC_rbf
from tools.machine_learning.SVC_sigmoid import SVC_sigmoid
from tools.machine_learning.data_holder import data_holder
from tools.machine_learning.Bayes_Ridge_Reg import Bayes_Ridge_Reg
from tools.machine_learning.Logistic_Reg import Logistic_Reg
from tools.machine_learning.ARD_Reg import ARD_Reg
from tools.machine_learning.Perceptron import Perceptron
from tools.machine_learning.Pas_agg_class import Pas_agg_class
from tools.machine_learning.KNeighborsClassifier import KNeighborsClassifier
from tools.machine_learning.Pipe_LinearSVC_KBest import Pipe_LinearSVC_KBest


#Deadline reached auf positiv setzen
#werte durchgehen
#    Waehrend deadline reached positiv 
#        berechne fuer aktuellen task ob erfolgreiche ausfuehrung
#        falls nicht deadline negativ setzen
#
#Spass mit der DB


#Define IDs of the tasks
TASK_LIST = {'hey': 1,
             'namaste': 2,
             'tumatmul': 3,
             'linpack': 4,
             'pi': 5,
             'cond_42': 6,
             'cond_mod': 7,
             }
BINARY_NAMES=[]




def read_input(file, tmp_list):
    if(os.path.exists(file)):
        print "Processing file "+file
        
        xml_root = xml.etree.ElementTree.parse(file).getroot()
        tmp_task_list = xml_root.findall('periodictask')
        
        
        for task in tmp_task_list:
            id =  int(task.find('id').text)
            #Check if id and binary which where send to genode is correct
            pkg = task.find('pkg').text
            real_id = TASK_LIST.get(pkg)
            if (id != real_id):
                raise Exception("Error in input file! Found ID "+str(id)+ " but should be "+ str(real_id)+ "for task "+pkg+"! Exit...")
            
            period = int(task.find('period').text)
            priority = int(task.find('priority').text)
            criticaltime = int(task.find('criticaltime').text)
            ram_quota = int(task.find('quota').text[:-1])
            
            
            arg = []
            
            for arg in task.find('config'):
                arg.append(arg.text)
                
                
            # periode, priority, critical_time, argument[0], ramquota 
            
            tmp_list.append((id, period, priority, criticaltime, int(arg[0]), ram_quota))
            
            

            
        print "\n"  
        
    else:
        print "Cannot read input file"



def read_output(file):
    if(os.path.exists(file)):
        print "Processing file "+file
        #magic
        xml_root = xml.etree.ElementTree.parse(file).getroot()

        task_list = xml_root.find('task-descriptions')
        
        for task in task_list:
            att_list = task.attrib
            for element in BINARY_NAMES:
                if element in att_list['thread']: 
                    if "1" in att_list['state']:
                        # Berechne deadline=task_start+task critical time
                        # Wenn deadline - finish time >= 10 ms -> deadline reached = 1
                        # else 0
                        
                        #tmp_tuple.append(()))
                        
                        if(att_list['execution-time']>100):
                            return False
                        
                        print "Task: "+element+" arrival_time: "+str(att_list['arrival-time'])+" execution_time: "+str(att_list['execution-time'])+" state: "+str(att_list['state'])
                        
        print "\n"  
        
        return True
    else:
        raise Exception("Cannot read output file")


def save_to_db(my_db, tuple):
    # Write tmp_data to db
    output("Write tmp data to database!")
    my_db.write(tuple)





#Generate binary names
for i in TASK_LIST:
    BINARY_NAMES.append("0"+str(TASK_LIST.get(i))+"."+i)


print BINARY_NAMES



genode_input ="../task_xml/task_v1.xml"
genode_output = "../log_profile.xml"
db_input = []



#Es veraendert sich periode, Argument, Prioritaet, critical_time
#Zu jeden input file nur ein output file!

#layout eines tasks: periode, priority, critical_time, argument[0], ramquota 

tmp_input_list = []

read_input(genode_input, tmp_input_list)

for i in range(0,7):
    #print tmp_input_list[i]
    tmp_col = []
    for tmp_task in tmp_input_list:
        tmp_col.append(tmp_task[0])
     
    if(not ((i+1) in tmp_col)):
        tmp_input_list.append(((i+1),0,0,0,0,0))
        

tmp_input_sort = sorted(tmp_input_list, key=lambda tup: tup[0])

tmp_db_input = []
for i in tmp_input_sort:
    counter=0
    for j in i:
        if counter != 0:
            tmp_db_input.append(j)
        counter+=1    
        
        




tmp_db_input.append(read_output(genode_output))

db_input.append(tuple(tmp_db_input))



my_db = db("ml_db.db",
           ["T1_Periode", "T1_Priority", "T1_Critical_Time", "T1_Arg", "T1_Ram_quota_in_M",
            "T2_Periode", "T2_Priority", "T2_Critical_Time", "T2_Arg", "T2_Ram_quota_in_M",
            "T3_Periode", "T3_Priority", "T3_Critical_Time", "T3_Arg", "T3_Ram_quota_in_M",
            "T4_Periode", "T4_Priority", "T4_Critical_Time", "T4_Arg", "T4_Ram_quota_in_M",
            "T5_Periode", "T5_Priority", "T5_Critical_Time", "T5_Arg", "T5_Ram_quota_in_M",
            "T6_Periode", "T6_Priority", "T6_Critical_Time", "T6_Arg", "T6_Ram_quota_in_M",
            "T7_Periode", "T7_Priority", "T7_Critical_Time", "T7_Arg", "T7_Ram_quota_in_M",
            "Deadline_reached"],
           
           ["int", "int", "int", "int", "int",
            "int", "int", "int", "int", "int", 
            "int", "int", "int", "int", "int", 
            "int", "int", "int", "int", "int", 
            "int", "int", "int", "int", "int", 
            "int", "int", "int", "int", "int", 
            "int", "int", "int", "int", "int",  
            "bool"])

print db_input

my_db.write(db_input)


#Hier muessen mehrere run betrachtet werden 
#read_output(genode_output)




    

#my_db = db("test_db.db",
#           ["Period1", "Period2", "Deadline_Reached"],
#           ["int", "int", "bool"])
    
    
    
    








