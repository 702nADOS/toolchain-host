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
    def read_input(self, genode_input, suc_table = "none"):
        tmp_input_list = []
        tmp_db_input = []
    
    
        #if file exists start parsing
        if(os.path.exists(genode_input)):            
            xml_root = xml.etree.ElementTree.parse(genode_input).getroot()
            tmp_task_list = xml_root.findall('periodictask')
            
            #for each tasks in the xml file get all parameters
            for task in tmp_task_list:
                binary_name = task.find('pkg').text
                
                id =  int(self.TASK_LIST[binary_name])
                #Check if id and binary which where send to genode is correct
                pkg = task.find('pkg').text
                real_id = self.TASK_LIST.get(pkg)
                #if (id != real_id):
                #    raise Exception("Error in input file! Found ID "+str(id)+ " but should be "+ str(real_id)+ "for task "+pkg+"! Exit...")
                
                task_id=period = int(task.find('id').text)
                period = int(task.find('period').text)
                priority = int(task.find('priority').text)
                criticaltime = int(task.find('criticaltime').text)
                ram_quota = int(task.find('quota').text[:-1])
                
                task_name=str(task_id)+"."+pkg
                if(task_id<10):
                    task_name="0"+task_name
                
                suc_finished=False
                if(not(suc_table=="none")):
                    if task_name in open(suc_table).read():
                        suc_finished=True
                    
                
                arg = []
                #read all arguments of a task
                for arg in task.find('config'):
                    arg.append(arg.text)
                    
                #append task to tmp_input_list
                #print genode_input
                tmp_input_list.append((id, period, priority, criticaltime, int(arg[0]), ram_quota, suc_finished))
                
                
             
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
                    tmp_input_list.append(((i+1),0,0,0,0,0, True))
                    
            #Sort the tasks to be in format t1,t2,...tn
            tmp_input_sort = sorted(tmp_input_list, key=lambda tup: tup[0])   
                               
            
            
            success=True
            
            #Loop over all tasks and parse them into one list
            for i in tmp_input_sort:
                counter=0
                
                if(not(i[-1])):
                    success=False
                    
                for j in i[:-1]:
                    if counter != 0:
                        tmp_db_input.append(j)
                    counter+=1   
                
            tmp_db_input.append(success)
                    
        
        else:
            raise Exception("Cannot read input file")
        
        return tmp_db_input
    
    
    #"""
    #Read in output genode file and determine deadline reached. This function returns True if the deadline is reached and false otherwise.
    #"""
    #def read_output(self, tmp_db_input, suc_table):
    #    if(os.path.exists(suc_table)):
    #        print tmp_db_input
    #        print suc_table
    #        
    #        #for task in tmp_task_list:                
    #        #    criticaltime = int(task.find('criticaltime').text)       
    #            #print "criticaltime "+str(criticaltime)
    #            #print "execution time "+str(execution_time)   
    #        #    if(run_time>criticaltime):
    #        #        return False
    #        
    #        #return True
    #        return False
    #    else:
    #        raise Exception("Cannot read output file")
    
    
    """
    input_files is a list of tuples in format [(input_genode_file1, output_genode_file1), (...)]
    """
    def save_into_db(self, input_files, suc_table):
        self.db_input = []
        
        for files in input_files:
            #print "Processing: \nInput_file"+files +"\n"
            #split the tuple
            #genode_input = files[0]
            #execution_time = files[1]
        
            #read in genode input file
            tmp_db_input = self.read_input(files, suc_table)
            
            #read in genode output file
            #tmp_db_input.append(self.read_output(tmp_db_input, suc_table))
            self.db_input.append(tmp_db_input)
        
        
        
        #print "Done processing all input file"
        
        print "DB input is "+str(self.db_input)
        
        #write all generated data into the database
        self.db.append(self.db_input)
        
        

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
        if(os.path.isfile(input_file)):
            #Remove true or false after this line
            #This is needed we are using read_input at multiple places
            ml_input = self.read_input(input_file)[:-1]
            print "Predict data "+str(ml_input)
            for algo in self.ml_algo:
                print str(algo)+" predicts "+str(algo.predict(ml_input))
        else:
            print "File "+input_file+" do not exists"

