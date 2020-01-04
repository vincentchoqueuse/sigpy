from .base import Processor,Connection
import numpy as np
from scipy.stats import norm
import time


class SequentialProcessor():
    
    """
        Blah blah blah.
        Parameters
        ---------
        name
        A string to assign to the `name` instance attribute.
        """
    
    def __init__(self,processors=[],connections=[],name="chain"):
        self._index = 0
        self.processors = processors
        self.connections = connections
        self.name = name
    
    def reset(self):
        self.processors = []
        self.connections = []
    
    def get_processor_by_name(self,name):
        processor = None
        for processor_temp in self.processors:
            if processor_temp.get_name() == name:
                processor = processor_temp
        return processor
    
    def get_processor_by_id(self,id):
        return self.processors[id]

    def add(self,processor):
        self.processors.append(processor)
    
    def get_connection(self,index):
        return self.connections[index]

    def add_connection(self,source,destination):
        connection = Connection(source[0],source[1],destination[0],destination[1])
        self.connections.append(connection)

    def show(self):
        for id,processor in enumerate(self.processors):
            print("processor {}: {}".format(id,processor.get_name()))
        for id,connection in enumerate(self.connections):
            print("connection {}: {}".format(id,connection.get_name()))

    
    def prepare(self):
        for processor in self.processors:
            processor.propagate = False
    
    
    def process(self,data=None):
        
        self.prepare()
        
        for processor in self.processors:
            start_time = time.time()
            data = processor.process(data)
            stop_time = time.time()
            processor.elapsed_time = stop_time-start_time
            
            for connection in self.connections:
                if connection.sender == processor:
                    connection.propagate()
        
        return data


class Generator(Processor):
    
    def __init__(self,data,N=None,name=None):
        super().__init__()
        self.data = data
        self.N = len(data)
        self.name = name
    
    def process(self,data=None):
        N = self.N
        data = self.data[:N]
        return data

class Recorder(Processor):

    def __init__(self,name=None):
        super().__init__()
        self.name = name
        self.data = []

    def process(self,data):
        self.data = data
        return data

class Linear_Channel(Processor):

    def __init__(self,H_tot,N=None,name=None):
        self.H_tot = H_tot
        self.N = N
        self.name = name

    @property
    def H(self):
        if self.N==None:
            H = self.H_tot
        else:
            H = self.H_tot[:self.N,:]
        return H

    def process(self,data):
        data = np.dot(self.H,data)
        return data

class Noise(Processor):

    def __init__(self,sigma2=0,seed=None,type="auto",name=None):
        self.sigma2 = sigma2
        self.name = name
        self.seed = seed
        self.type = type
    
    def get_type(self,data):
        if self.type is not "auto":
            type = self.type
        else:
            if np.iscomplexobj(data):
                type = "complex"
            else:
                type = "real"
        return type

    def process(self,data):
        type = self.get_type(data)
        N = len(data)
        if type == "real":
            noise = np.sqrt(self.sigma2)*norm.rvs(size=N)
        else:
            noise = np.sqrt(self.sigma2/2)*(norm.rvs(size=N)+1j*norm.rvs(size=N))
        data = data + noise
        return data



