import os, sys
sys.path.append("..")

from sigpy.core import Generator, Linear_Channel, Noise, Linear_Estimator, SequentialProcessor, Estimator_Metric
from sigpy.simulations import Monte_Carlo_Scenario
import numpy as np
from scipy.stats import norm
import numpy.linalg as lg
import matplotlib.pyplot as plt


class MSE_bound():
    
    def __init__(self,channel,noise,name="mse bound"):
        self.channel = channel
        self.noise = noise
        self.name = name

    def evaluate(self):
        H = self.channel.H
        sigma2 = self.noise.sigma2
        C = sigma2*lg.inv(np.dot(np.transpose(H),H))
        return np.diag(C)

# General Parameters
generator = Generator(norm.rvs(size=3))
channel = Linear_Channel(norm.rvs(size=(100,3)))
noise = Noise()
estimator = Linear_Estimator(channel.H)
processor = SequentialProcessor([generator,channel,noise,estimator])

# Monte Carlo
metric = Estimator_Metric(estimator,true_value = generator.data)
bound = MSE_bound(channel,noise)

mc = Monte_Carlo_Scenario(processor)
mc.set_scenario([noise],"sigma2",np.arange(0.1,1.4,0.1))
mc.add_theoretical(bound)
mc.evaluate([metric], 1000)
mc.plot()
plt.show()
