import time

from sklearn import linear_model

from data_holder import data_holder
import numpy as np


class SGD(data_holder):
    def __init__(self):
        self.algo_name = "SGD"
                
        indv_start = time.time()
        
        self.ml_algo = linear_model.SGDClassifier(
            loss="log",  # hinge, log, modified_huber, squared_hinge, perceptron, squared_loss, huber, epsilon_insensitive, squared_epsilon_insensitive
            penalty="l1",
            alpha=0.0001,
            l1_ratio=0.15,
            fit_intercept=True,
            n_iter=10,
            shuffle=True,
            verbose=0,
            epsilon=0.1,
            n_jobs=1,
            random_state=None,
            learning_rate="constant",
            eta0=0.001,
            power_t=0.05,
            class_weight={1:30},
            warm_start=False,
            average=True
        )
        
        self.fit()
        
        indv_end = time.time()
        
        self.output(" Initialized in " + str(indv_end - indv_start) + " sec")        
