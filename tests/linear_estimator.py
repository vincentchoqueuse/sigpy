import os, sys
sys.path.append("..")

from sigpy.core import Generator, Linear_Channel, Noise, Linear_Estimator, SequentialProcessor, Estimator_Metric, Theoretical_Metric
from sigpy.simulations import Monte_Carlo
import numpy as np
from scipy.stats import norm
import numpy.linalg as lg
import matplotlib.pyplot as plt


class MSE_bound(Theoretical_Metric):

    def evaluate(self):
        H = self.H[:self.N,:]
        C = self.sigma2*lg.inv(np.dot(np.transpose(H),self.H))
        return np.diag(C)

# General Parameters
x = norm.rvs(size=3)
H = norm.rvs(size=(100,3))

generator = Generator(x)
channel = Linear_Channel(H)
noise = Noise(sigma2=0)
estimator = Linear_Estimator(H,name="est")
processor =  SequentialProcessor([generator,channel,noise,estimator])

# Monte Carlo
metric = Estimator_Metric(true_value=x)
bound = MSE_bound(H=H,sigma2=0,N=100,name = "mse")

mc = Monte_Carlo(nb_trials = 1000)
mc.set_processor(processor)
mc.add_metric(metric)
mc.add_bound(bound)
mc.add_context_connection(noise,"sigma2")
mc.add_context_connection(bound,"sigma2")
mc.add_connection(estimator,"estimate",metric,"collected_data")

x_vect = np.arange(0.2,1.4,0.2)
mc.run(x_vect)
mc.plot()
plt.legend()
plt.show()
