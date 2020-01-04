from sigpy.core import Connection, Dataset, Metric
import numpy as np
import matplotlib.pyplot as plt



class Monte_Carlo():
    
    '''
        The Single Monte_Carlo object is used to perform a Monte Carlo Simulation.
        
        Monte Carlo simulations are based on a context object that manages the simulation. This context manages the connections to add before the simulation (method `add_context_connection`)
        '''

    def __init__(self,processor):
        self.processor = processor
    
    def evaluate(self,metric_list,nb_trials=100):
        
        for metric in metric_list:
            metric.reset()
        
        for num_trial in range(nb_trials):
            self.processor.process()
            
            for metric in metric_list:
                metric.append()

        data = []
        for indice in range(len(metric_list)):
            metric_value = metric_list[indice].evaluate()
            data.append(metric_value)

        return data



class Monte_Carlo_Scenario():

    def __init__(self,processor):
        self.processor = processor
        self.theoretical_list = []
    
    def plot(self,x=None,legend=True):
        for dataset in self.dataset_list:
            dataset.plot(x=x)
        if legend == True:
            plt.legend()

    def set_scenario(self,receiver_list,parameter,param_values):
        self.receiver_list = receiver_list
        self.parameter = parameter
        self.param_values = param_values
    
    def add_theoretical(self,theoretical):
        self.theoretical_list.append(theoretical)
    
    def evaluate(self,metric_list,nb_trials=100):
        
        dataset_list = []
        theoretical_list = self.theoretical_list
        
        for metric in metric_list + theoretical_list:
            dataset = Dataset(figure_num=1,name=metric.name)
            dataset.set_header(self.param_values)
            dataset_list.append(dataset)
        
        mc = Monte_Carlo(self.processor)
        for indice in range(len(self.param_values)):

            param_value = self.param_values[indice]
            
            print("* Parameter Value: {} ".format(param_value))
            
            for receiver in self.receiver_list:
                setattr(receiver,self.parameter,param_value)
            
            data = mc.evaluate(metric_list,nb_trials=nb_trials)
            
            #add theoretical values
            for theoretical in theoretical_list:
                data.append(theoretical.evaluate())
        
            for indice in range(len(data)):
                dataset_list[indice].append(data[indice])

        self.dataset_list = dataset_list


