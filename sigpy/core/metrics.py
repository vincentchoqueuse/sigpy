from .base import Metric
import numpy as np
import numpy.linalg as lg

class Time_Metric(Metric):

    def __init__(self,processor,attribute,type = "mean",name = None):
        self.processor = processor
        self.attribute = attribute
        self.time_elapsed = []
        self.name = name
    
    def get_name(self):
        if self.name is None:
            name = self.processor.get_name()
        else:
            name = self.name
        return name
    
    def update(self):
        value = getattr(self.processor,self.attribute)
        self.time_elapsed.append(value)
    
    def evaluate(self):
        if type == "mean":
            value = np.mean(self.time_elapsed)
        return value


class Estimator_Metric(Metric):

    def __init__(self,true_value,estimate=[],type = "MSE",name = None):
        self.true_value = true_value
        self.estimate = estimate
        self.type = type
        self.name = name
        self.collected_data = []
    
    def reset(self):
        self.estimate = []
        self.collected_data = []
    
    def get_name(self):
        return self.name

    def append(self):
        self.estimate.append(self.collected_data)
        self.collected_data = []
    
    def evaluate(self):
        if self.type == "MSE":
            value = np.mean((self.true_value - self.estimate)**2,axis = 0)
        return value


class Theoretical_Metric(Metric):

    def __init__(self,**kwargs):
        for arg in kwargs:
            setattr(self,arg,kwargs[arg])
    
    def evaluate(self):
        H = self.H[:self.N,:]
        H_T = np.transpose(H)
        C = self.sigma2*lg.inv(np.dot(H_T,self.H))
        value = np.diag(C)
        return value




