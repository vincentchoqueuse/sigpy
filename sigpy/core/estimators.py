from .base import Processor
import numpy as np
from numpy.linalg import pinv

class Estimator(Processor):
    
    propagate = True

    def __init__(self,name = "estimator"):
        self.name = name

    def process(self,data):
        value = self.fit(data)
        self.estimate = value
        return data

class Linear_Estimator(Estimator):
    
    def __init__(self,H,name="linear estimator"):
        self.name = name
        self.H = H

    def fit(self,data):
        N = len(data)
        H_pinv = pinv(self.H[:N,:])
        value = np.dot(H_pinv,data)
        return value
