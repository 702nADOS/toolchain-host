import random
import time
import os.path, sys
from tools.db import db
import xml.etree.ElementTree
from dns.rdatatype import NULL
from tools.machine_learning.data_holder import data_holder



class ml:
    #Define IDs of the tasks
    TASK_LIST = {'hey': 1,
                 'namaste': 2,
                 'tumatmul': 3,
                 'linpack': 4,
                 'pi': 5,
                 'cond_42': 6,
                 'cond_mod': 7
                }
    BINARY_NAMES=[]
    db_input = []
    data_holder = NULL
    #list of ml algorithmens
    ml_algo = []

    def __init__(self, database_path):
        #Generate binary names
        for i in self.TASK_LIST:
            self.BINARY_NAMES.append("0"+str(self.TASK_LIST.get(i))+"."+i)
            
        db_header = []
        db_header_type = []
        
        #generate db headers and types
        for i in range(0, len(self.TASK_LIST)):
            db_header.append("T"+str(i)+"_Periode")
            db_header.append("T"+str(i)+"_Priority")
            db_header.append("T"+str(i)+"_Critical_Time")
            db_header.append("T"+str(i)+"_Arg")
            db_header.append("T"+str(i)+"_Ram_quota_in_M")
            
            for z in range(0,5):
                db_header_type.append("int")
            
        db_header.append("Deadline_reached")
        db_header_type.append("bool")
        
        #open database for writing
        self.db = db(database_path, db_header, db_header_type)
    
    """
    genode_input := read in genode input file
    """
    def read_input(self, genode_input):
        tmp_input_list = []
        tmp_db_input = []
    
    
        #if file exists start parsing
        if(os.path.exists(genode_input)):            
            xml_root = xml.etree.ElementTree.parse(genode_input).getroot()
            tmp_task_list = xml_root.findall('periodictask')
            
            #for each tasks in the xml file get all parameters
            for task in tmp_task_list:
                id =  int(task.find('id').text)
                #Check if id and binary which where send to genode is correct
                pkg = task.find('pkg').text
                real_id = self.TASK_LIST.get(pkg)
                if (id != real_id):
                    raise Exception("Error in input file! Found ID "+str(id)+ " but should be "+ str(real_id)+ "for task "+pkg+"! Exit...")
                
                period = int(task.find('period').text)
                priority = int(task.find('priority').text)
                criticaltime = int(task.find('criticaltime').text)
                ram_quota = int(task.find('quota').text[:-1])
                
                
                arg = []
                #read all arguments of a task
                for arg in task.find('config'):
                    arg.append(arg.text)
                    
                #append task to tmp_input_list
                tmp_input_list.append((id, period, priority, criticaltime, int(arg[0]), ram_quota))
                
             
            """ 
            fill in all tasks which where not used in this task
            for example if task 3 and 2 are defined in the input xml file the output would be for a total number of four tasks
            [(2,x,x,x,x,x),
             (3,x,x,x,x,x),
             (1,0,0,0,0,0),
             (4,0,0,0,0,0)]
            """
            for i in range(0,len(self.TASK_LIST)):
                #print tmp_input_list[i]
                tmp_col = []
                for tmp_task in tmp_input_list:
                    tmp_col.append(tmp_task[0])
                 
                if(not ((i+1) in tmp_col)):
                    tmp_input_list.append(((i+1),0,0,0,0,0))
                    
            #Sort the tasks to be in format t1,t2,...tn
            tmp_input_sort = sorted(tmp_input_list, key=lambda tup: tup[0])   
                    
            
            #Loop over all tasks and parse them into one list
            for i in tmp_input_sort:
                counter=0
                for j in i:
                    if counter != 0:
                        tmp_db_input.append(j)
                    counter+=1   
        
        else:
            raise Exception("Cannot read input file")
        
        return tmp_db_input
    
    
    """
    Read in output genode file and determine deadline reached. This function returns True if the deadline is reached and false otherwise.
    """
    def read_output(self, file):
        if(os.path.exists(file)):
            
            xml_root = xml.etree.ElementTree.parse(file).getroot()
    
            task_list = xml_root.find('task-descriptions')
            
            for task in task_list:
                att_list = task.attrib
                for element in self.BINARY_NAMES:
                    if element in att_list['thread']: 
                        if "1" in att_list['state']:                            
                            print "Task: "+element+" arrival_time: "+str(att_list['arrival-time'])+" execution_time: "+str(att_list['execution-time'])+" state: "+str(att_list['state'])
                            
                            
                            """
                            TODO:
                            Auslesen der finishing time und setzen von deadline reached
                            """
                            if(int(att_list['execution-time'])>1000):
                                return False
            
            return True
        else:
            raise Exception("Cannot read output file")
    
    
    """
    input_files is a list of tuples in format [(input_genode_file1, output_genode_file1), (...)]
    """
    def save_into_db(self, input_files):
        
        for files in input_files:
            print "Processing: \nInput_file"+files[0] +"\nOutput_file"+ files[1]+"\n"
            #split the tuple
            genode_input = files[0]
            genode_output = files[1]
        
            #read in genode input file
            tmp_db_input = self.read_input(genode_input)
            
            #read in genode output file
            tmp_db_input.append(self.read_output(genode_output))
            self.db_input.append(tuple(tmp_db_input))
            
        
        #write all generated data into the database
        self.db.write(self.db_input)
        

    """
    Set machine learning algorithmens
    """
    def set_ml_algos(self, ml_algo):
        self.ml_algo=ml_algo

    """
    Read all data from the database and store it into a dataholder
    """
    def read_from_db(self):
        if (len(self.db_input)<1):
            raise Exception("No data available in db_input.")
        
        # Get output and input data from db
        output_data = self.db.read_deadline_reached()
        input_data = self.db.read_task_input()
        
        data_per_set = len(self.db.attr)
        num_trainingsets = len(self.db_input)
                        
        self.data_holder = data_holder(data_per_set, num_trainingsets, input_data, output_data)       


    """
    Save all machine learning algorithms into a pickle file
    """
    def save_pickle(self, pickle_path):
        for algo in self.ml_algo:
            algo.save(pickle_path)
            
    """
    Load all machine learning algorithmens from a pickle file
    """
    def load_pickle(self, pickle_path):        
        for algo in self.ml_algo:
            algo.load(pickle_path)
        
        
    """
    Predict for each machine learning algorithmen if the task can reach its deadline
    """
    def predict(self, input_file):
        ml_input = self.read_input(input_file)
        print "Predict data "+str(ml_input)
        for algo in self.ml_algo:
            print str(algo)+" predicts "+str(self.ml_algo[0].predict(ml_input))

