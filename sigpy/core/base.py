import numpy as np
import inspect
import time
import matplotlib.pyplot as plt


class Connection():

    def __init__(self,source,attribute_s,destination,attribute_d=None):
        if attribute_d == None:
            attribute_d = attribute_s
        
        self.source = source
        self.attribute_s = attribute_s
        self.destination = destination
        self.attribute_d = attribute_d

    def get_name(self):
        return "sender={} ({}) -> destination={} ({})".format(self.source.get_name(),self.attribute_s,self.destination.get_name(),self.attribute_d)
        
    def propagate(self,force=True):
        if (self.source.propagate) or (force==True):
            attribute = getattr(self.source, self.attribute_s)
            setattr(self.destination,self.attribute_d,attribute)

    def show(self):
        print("Connection: {}".format(self.get_name()))


class Processor():
    
    '''
        The Processor object can be used to process a signal
        
        Args:
        path (str): The path of the file to wrap
        field_storage (FileStorage): The :class:`FileStorage` instance to wrap
        temporary (bool): Whether or not to delete the file when the File
        instance is destructed
        
        Returns:
        BufferedFileStorage: A buffered writable file descriptor
        '''
    
    
    def __init__(self,name = "processor"):
        self.name = name
    
    def get_name(self):
        if self.name is not None:
            name = self.name
        else :
            name = self.__class__.__name__
        return name
    
    def process(self,data):
        return data



class Metric():

    '''
    The Metric object can be used to compute a metric
    '''

    def __init__(self,name = None,unit=None):
        self.value = None
        self.name = name
        self.unit = unit
        self.data = []

    def get_name(self):
        name = self.name
        if name is None:
            name = self.__class__.__name__
        return name

    def reset(self):
        self.data = []
    
    def collect(self,data):
        self.data.append(data)

    def evaluate(self):
        pass


class Dataset():
    
    '''
        The Dataset object is used to store different values
    '''

    def __init__(self,figure_num=None,name=None):
        self.header = []
        self.name = name
        self.data = []
        self.figure_num = figure_num
    
    def reset(self):
        self.data = data
    
    def length():
        return len(self.data)
    
    def set_header(self,header):
        self.header = header
    
    def get_header(self):
        if self.header is None:
            header = range(len(self.data))
        else:
            header = self.header
        return header
    
    def get_name(self):
        name = self.name
        if name is None:
            name = self.__class__.__name__
        return name
    
    def append(self,data_temp,header_temp=None,verbose=True):
        self.data.append(data_temp)
        if verbose == True :
            print("Dataset ({}): {}".format(self.get_name(),data_temp))

    def show(self):
        header = self.get_header()
        
        print("Dataset {}".format(self.get_name()))
        for indice in range(len(self.data)):
            data = self.data[indice]
            print("{}: {}".format(header[indice],data))

    def plot(self,x=None):
        plt.figure(self.figure_num)
        if x is None:
            x = self.get_header()
        plt.plot(x,self.data,label=self.get_name())



