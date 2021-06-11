import numpy as np


def constant(temperature, a, i):
    return temperature


def logarithmic(temperature, a, i):
    return (temperature / (1 + a*np.log(1 + i)))


def exponential(temperature, a, i):
    return (temperature * a ** i)



def hyperbolic(temperature, a, i):
    return (temperature / (1 + a * i))
