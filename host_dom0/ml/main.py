from tools.machine_learning.ml import ml
import os
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
import sys
import xml.etree.ElementTree
import re


print "Welcome to main"
#Generate machine learning database
ml = ml("ml_db.db")


files = []

taskset_groups=[
                ("../task_xml/done/condmod_run1/cond_mod","../task_xml/done/condmod_run1/suc_tasks.log"),
                ("../task_xml/done/condmod_run2/cond_mod","../task_xml/done/condmod_run2/suc_tasks.log"),
                ("../task_xml/done/hey_pi_run1/hey_pi","../task_xml/done/hey_pi_run1/suc_tasks.log"),
                ("../task_xml/done/hey_tum_run1/hey_tumatmul","../task_xml/done/hey_tum_run1/suc_tasks.log"),
                ("../task_xml/done/hey_tum_run2/hey_tumatmul","../task_xml/done/hey_tum_run2/suc_tasks.log"),
                ("../task_xml/done/linpack_run1/linpack","../task_xml/done/linpack_run1/suc_tasks.log"),
                ("../task_xml/done/linpack_run2/linpack","../task_xml/done/linpack_run2/suc_tasks.log"),
                ("../task_xml/done/linpack_run3/linpack","../task_xml/done/linpack_run3/suc_tasks.log"),
                ("../task_xml/done/linpack_run4/linpack","../task_xml/done/linpack_run4/suc_tasks.log"),
                ("../task_xml/done/hey_lin_run1/hey_linpack","../task_xml/done/hey_lin_run1/suc_tasks.log"),
                ("../task_xml/done/hey_run1/hey","../task_xml/done/hey_run1/suc_tasks.log"),
                ("../task_xml/done/lin_pi_run1/linpack_pi","../task_xml/done/lin_pi_run1/suc_tasks.log"),
                ("../task_xml/done/lin_pi_run2/linpack_pi","../task_xml/done/lin_pi_run2/suc_tasks.log"),
                ("../task_xml/done/lin_pi_run3/linpack_pi","../task_xml/done/lin_pi_run3/suc_tasks.log"),
                ("../task_xml/done/namaste_run1/namaste","../task_xml/done/namaste_run1/suc_tasks.log"),
                ("../task_xml/done/pi_run1/pi","../task_xml/done/pi_run1/suc_tasks.log"),
                ("../task_xml/done/tumatmul_run1/tumatmul","../task_xml/done/tumatmul_run1/suc_tasks.log"),
                ("../task_xml/done/tumatmul_run2/tumatmul","../task_xml/done/tumatmul_run2/suc_tasks.log"),
                ("../task_xml/done/tum_lin_run1/tumatmul_linpack","../task_xml/done/tum_lin_run1/suc_tasks.log"),
                ("../task_xml/done/tum_pi_hey_run1/tumatmul_pi_hey","../task_xml/done/tum_pi_hey_run1/suc_tasks.log"),
                ("../task_xml/done/tum_pi_lin_hey_cmod_mod42_run1/tumatmul_pi_linpack_hey_cond_mod_cond_42","../task_xml/done/tum_pi_lin_hey_cmod_mod42_run1/suc_tasks.log"),
                ("../task_xml/done/tum_pi_lin_run1/tumatmul_pi_linpack","../task_xml/done/tum_pi_lin_run1/suc_tasks.log"),
                ("../task_xml/done/tum_pi_run1/tumatmul_pi","../task_xml/done/tum_pi_run1/suc_tasks.log"),
                
                
                
                
                ]

print "\n##################"
print "Saving data into DB"
print "###################"

print "Start processing tasksets \n"+str(taskset_groups)+"\n"
for taskset in taskset_groups:
    counter=0
    files=[]
    
    if(not(os.path.isfile(taskset[0]+str(counter)+".xml"))):
        print "Could not access taskset file! "+taskset[0]+str(counter)+".xml"
    
    #generate tubles of input and output files
    while (os.path.isfile(taskset[0]+str(counter)+".xml") ):
        
        files.append( taskset[0]+str(counter)+".xml" )
        counter+=1
    
    
    
    #save all input and output files to database
    ml.save_into_db(files, taskset[1])

print "Done saving all tasksets into db"





"""
print "\n###########"
print "Train data"
print "###########"
#train the database from the written db
ml.read_from_db()


ml_algo = []
#generate a list of all ml algorithmen
svc_linear = SVC_linear()
svc_rbf = SVC_rbf()
svc_sigmoid = SVC_sigmoid()
sgd = SGD()
bay_reg = Bayes_Ridge_Reg()
log_reg = Logistic_Reg()
percep = Perceptron()
pas_agg_class = Pas_agg_class()
k_neigh = KNeighborsClassifier()

#append ml algorithms to a list
ml_algo.append(svc_linear)
ml_algo.append(svc_rbf)
ml_algo.append(svc_sigmoid)
ml_algo.append(sgd)
ml_algo.append(bay_reg)
ml_algo.append(log_reg)
ml_algo.append(percep)
ml_algo.append(pas_agg_class)
ml_algo.append(k_neigh)

#save the lis
ml.set_ml_algos(ml_algo)

#save trained ml algorithms to file
ml.save_pickle("pickle_")


print "\n#############"
print "Load pickle files"
print "#############"
#load already trained ml algorithms from file
ml.load_pickle("pickle_")

print "\n#############"
print "Predict data"
print "#############"
#predict an input xml files
for i in range(0, 9999):
    ml.predict("../task_xml/pi_run_test/pi"+str(i)+".xml")


"""




