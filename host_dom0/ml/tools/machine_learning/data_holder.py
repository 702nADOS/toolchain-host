import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cbook import Null
from sklearn.externals import joblib
from pyanaconda.iutil import DataHolder
import os


if False: plt=None

class data_holder:
    #static variables
    input_2dvector = None# Input parameter
    output_1dvector = None # Output parameter
    data_per_set = 0 # amount of values per training tuple
    X_new = None
    algo_name="Data_holder"
    
    #Instance of this ml algorithm
    ml_algo = Null
    
    
    def __init__(self, data_per_set, AmountRows, data_input, data_output):
        #define static variables which are equal to all algorithmns
        data_holder.input_2dvector = np.ndarray(shape=(AmountRows,data_per_set-1)) # Input parameter
        data_holder.output_1dvector = np.ndarray(shape=[AmountRows]) # Output parameter
        data_holder.data_per_set = data_per_set-1 # dimensions of plot and data
        data_holder.X_new = Null
        
        self.output("Load training data")
        # get data
        data_holder.input_2dvector = np.array(data_input)
        data_holder.output_1dvector = np.ravel(np.array(data_output))
        
        
        # output method
    def output(self, msg):
        for line in msg.splitlines():
            print self.algo_name+": "+line
        
    def save(self, file_path):
        if self.ml_algo==Null:
            self.output("ML algorithm not initialized! Abort saving... ")
            return
        
        file_path+=self.algo_name
        #correct dataype if .pkl is missing
        if not(file_path[-4:]==".pkl"):
            file_path+=".pkl"
            
        self.output("Save training set to "+file_path)
        joblib.dump(self.ml_algo, file_path)
        
    def load(self, file_path):
        file_path+=self.algo_name
        
        #correct dataype if .pkl is missing
        if not(file_path[-4:]==".pkl"):
            file_path+=".pkl"
            
        if(not(os.path.isfile(file_path))):
            raise Exception("Cannot reach pickle file! "+file_path)
        
        self.output("Load training set")
        self.ml_algo = joblib.load(file_path) 
        
    #toString method
    def __repr__(self):
        return self.algo_name
    
    def get_ml_algo(self):
        return self.ml_algo
    
    def fit(self):
        if(not(data_holder.output_1dvector is None)):
            self.ml_algo.fit(data_holder.input_2dvector,  data_holder.output_1dvector)
        
    def partial_fit(self, input_2dvector, output_1dvector):
        try:
            self.ml_algo.partial_fit(input_2dvector,  output_1dvector)
        except: 
            self.output("Can not partially fit data to this ml algorithm")
        
        
        
    """
    This function is obsolete
    """
    def plot(self, algo_list, plot_columns = 4, h=1, x_list_value=0, y_list_value=1):
        if(x_list_value==y_list_value):
            raise Exception("x_list_value must be different from y_list_value")        
        
        if not(isinstance(self, data_holder)):
            self.output("Plot can only be executed from data_holder!")
            return
        
        algo_list_length = len(algo_list)
        if algo_list_length < plot_columns:
            plot_columns=algo_list_length
        if algo_list_length<1:
            self.output("List is empty!")
            return
        
        self.output("Plotting data for "+str(algo_list))
        
        #
        #Initialize figure stuff 
        #
        plot_rows = ((algo_list_length-1)/plot_columns)+1   
        plt.figure(figsize=(plot_columns*3.5, plot_rows*3.5))
        
        #
        # Prepare the data 
        #
        # create a mesh to plot in, only if |input_2dvector data|==2
        
        
        #print "input_vector "+str(data_holder.input_2dvector)
        
        #input_vector = data_holder.input_2dvector[:, [x_list_value,y_list_value]]
        
        #for task in data_holder.input_2dvector:
        #    tmp_input_list = []
        #    tmp_input_list.append(data_holder.input_2dvector[x_list_value])
        #    tmp_input_list.append(data_holder.input_2dvector[y_list_value])
            #input_vector.append(tmp_input_list)
            
           
        print data_holder.input_2dvector[:, [x_list_value,y_list_value]]
        #print data_holder.output_1dvector
        
        x_min, x_max = input_vector[:, 0].min() - 50, input_vector[:, 0].max() + 50
        y_min, y_max = input_vector[:, 1].min() - 50, input_vector[:, 1].max() + 50
        
        #only plot results, if data equals 2. In other cases no proper visualisation is possible
        #if(self.data_per_set==2):
        #    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
        #else:
            #data_holder.output("data_per_set not equal 2. Abort plotting")
            #return
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
        
        #loop over the list
        for i in range(0, algo_list_length):
            plt.subplot(plot_rows, plot_columns, i + 1)
            plt.subplots_adjust(wspace=0.3, hspace=0.3)
            
            if not(algo_list[i]==None):
                algo = algo_list[i].get_ml_algo()
                    
                #mache zeugs
                if not(algo==Null):
                    Z_ = algo.predict(np.c_[xx.ravel(), yy.ravel()])
                    
                    # Put the result into a color plot
                    Z = Z_.reshape(xx.shape)
                    plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm_r, alpha=0.8)
                    plt.xlim(xx.min(), xx.max())
                    plt.ylim(yy.min(), yy.max())
              
                    # Plot also the training points
                    plt.scatter(input_vector[:, 0], input_vector[:, 1], c=data_holder.output_1dvector, cmap=plt.cm.coolwarm_r, alpha=0.5)  
                  
        
                    plt.xlabel("Period Task 1")
                    plt.ylabel("Period Task 2")
                else:
                    plt.xlabel("ML not initialized!") 
            else:
                plt.xlabel("ML not initialized!")   

            plt.xticks(())
            plt.yticks(())
            plt.title(algo_list[i])    
            
    
        plt.show()
        self.output("Plotting done!")
        
    def predict(self, input):
        ml_input = np.ravel(np.array(input)).reshape(1, -1)
               
        return self.ml_algo.predict(ml_input)
    
        
        