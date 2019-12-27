from sigpy.core import Connection, Dataset, Metric
import numpy as np
import matplotlib.pyplot as plt

class MC_context():

    def __init__(self):
        self.value = None
        self.propagate = True

    def get_name(self):
        return "mc_context"


class Single_Monte_Carlo():
    
    '''
        The Single Monte_Carlo object is used to perform a Monte Carlo Simulation.
        
        Monte Carlo simulations are based on a context object that manages the simulation. This context manages the connections to add before the simulation (method `add_context_connection`)
        '''

    def __init__(self,nb_trials = 1000):
        self.context = MC_context()
        self.nb_trials = nb_trials
        self.processor = []
        self.metrics = []
        self.bounds = []
        self.context_connections = []
        self.connections = []

    def prepare(self,param_value):
        self.data = []
        self.context.value = param_value
        for connection in self.context_connections:
            connection.propagate()
        
        for metric in self.metrics + self.bounds:
            metric.reset()

    def add_context_connection(self,destination,attribute):
        connection = Connection(self.context,"value",destination,attribute)
        self.context_connections.append(connection)

    def add_connection(self,source,attribute_source,destination,attribute_destination=None):
        if attribute_destination == None:
            attribute_destination = attribute_source
        connection = Connection(source,attribute_source,destination,attribute_destination)
        self.connections.append(connection)
        
        # store sender name to metric
        if isinstance(destination, Metric):
            destination.name = source.get_name()

    def add_metric(self,metric):
        self.metrics.append(metric)

    def add_bound(self,bound):
        self.bounds.append(bound)

    def set_processor(self,processor):
        self.processor = processor

    def show(self):
        print("-------- Processor --------")
        print(self.processor.show())
        print("--- Context Connections ---")
        for connection in self.context_connections:
            print(connection.show())
        print("------- Connections -------")
        for connection in self.connections:
            print(connection.show())

    def run(self,param_value):
        self.prepare(param_value)
        
        for num_trial in range(self.nb_trials):
            self.processor.process()
            for connection in self.connections:
                connection.propagate()
            
            for metric in self.metrics:
                metric.append()

        metrics_bounds = self.metrics + self.bounds
        for indice in range(len(metrics_bounds)):
            metric = metrics_bounds[indice]
            metric_value = metric.evaluate()
            self.data.append(metric_value)



class Monte_Carlo(Single_Monte_Carlo):

    def __init__(self,nb_trials = 1000):
        self.context = MC_context()
        self.nb_trials = nb_trials
        self.processor = []
        self.metrics = []
        self.bounds = []
        self.context_connections = []
        self.connections = []
        self.dataset = []

    def plot(self,x=None):
        for dataset in self.dataset:
            dataset.plot(x=x)

    def run(self,param_values):
        
        self.dataset = []
        
        for metric in self.metrics + self.bounds:
            dataset = Dataset(figure_num=1,name=metric.name)
            dataset.set_header(param_values)
            self.dataset.append(dataset)
        
        for indice in range(len(param_values)):
            super().run(param_values[indice])
        
            for indice in range(len(self.data)):
                self.dataset[indice].append(self.data[indice])



