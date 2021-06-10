import numpy as np


def constant(Temp_0):
    return Temp_0


def logarithmic(Temp_0, a, i):
    return (Temp_0 / (1 + a*np.log(1 + i)))


def exponential(Temp_0, a, i):
    return (Temp_0 * a ** i)



def hyperbolic(Temp_0, a, i):
    return (Temp_0 / (1 + a * i))
