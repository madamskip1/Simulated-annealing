import numpy as np
import math 

# wybrać kilka z:
# https://en.wikipedia.org/wiki/Test_functions_for_optimization


# Multi-dim
def rastrigin_function(dimArray):
    sumPart = 0
    
    for x in dimArray:
        sumPart += (x ** 2 - 10 * np.cos(2 * np.pi * x))
        
    rastrigin = 10 * len(dimArray) + sumPart

    return rastrigin

def rosenbrock_function(dimArray):
    rosenbrock = 0

    for i in range(len(dimArray)-1):
        rosenbrock += (100 * ((dimArray[i] - ( dimArray[i+1] ** 2 ) ) ** 2 + (1 - dimArray[i]) ** 2))

    return rosenbrock

# 2-dim
def ackley_function(dimArray):
    return ( (-20.0) * math.exp( (-0.2) * np.sqrt(0.5 * ( (dimArray[0] ** 2) + (dimArray[1] ** 2 )))) 
             - np.exp(0.5 * ( (np.cos(2*np.pi*dimArray[0])) + np.cos(2*np.pi*dimArray[1]) ))
             + np.e + 20.0 )


def levi_n13_function(dimArray):
    return ( np.sin(3*np.pi*dimArray[0]) ** 2 
             + ( (dimArray[0] -1) ** 2 ) * ( 1 + (np.sin(3*np.pi*dimArray[1]) ** 2) )
             + ( (dimArray[1] -1) ** 2 ) * ( 1 + (np.sin(2*np.pi*dimArray[1]) ** 2) ) 
            )
