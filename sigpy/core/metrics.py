from .base import Metric
import numpy as np
import numpy.linalg as lg

class Time_Metric(Metric):

    def __init__(self,processor,type = "mean",name = None):
        self.processor = processor
        self.time_elapsed = []
        self.type = type
        self.name = name
    
    def reset(self):
        self.time_elapsed = []
    
    def get_name(self):
        if self.name is None:
            name = self.processor.get_name()
        else:
            name = self.name
        return name
    
    def append(self):
        time_elapsed = getattr(self.processor,"time_elapsed")
        self.time_elapsed.append(time_elapsed)
    
    def evaluate(self):
        if type == "mean":
            value = np.mean(self.time_elapsed)
        return value


class Estimator_Metric(Metric):

    def __init__(self,estimator,true_value=None,type = "MSE",name = None):
        self.estimator = estimator
        self.true_value = true_value
        self.estimate = []
        self.type = type
        self.name = name
    
    def get_name(self):
        if self.name is None:
            name = self.estimator.get_name()
        else:
            name = self.name
        return name
    
    def reset(self):
        self.estimate = []

    def append(self):
        estimate = getattr(self.estimator,"estimate")
        self.estimate.append(estimate)
    
    def evaluate(self):
        if self.type == "MSE":
            value = np.mean((self.true_value - self.estimate)**2,axis = 0)
        return value






