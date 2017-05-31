from ml import ml
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


print "Welcome to main"
#Generate machine learning database
ml = ml("ml_db.db")


files = []
#pattern for input and output files
input_file_pattern="../task_xml/task"
output_file_pattern="../task_xml/log_task"

counter=0
#generate tubles of input and output files
while (os.path.isfile(input_file_pattern+str(counter)+".xml") and os.path.isfile(output_file_pattern+str(counter)+".xml")):
    tmp_tuple = (input_file_pattern+str(counter)+".xml", output_file_pattern+str(counter)+".xml")
    files.append( tmp_tuple )
    counter+=1

#save all input and output files to database
ml.save_into_db(files)



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
#ml.save_pickle("pickle_")


print "\n#############"
print "Load pickle files"
print "#############"
#load already traubed ml algorithmens fromfile
#ml.load_pickle("pickle_")

print "\n#############"
print "Predict data"
print "#############"
#predict an input xml files
ml.predict("../task_xml/task_test.xml")




