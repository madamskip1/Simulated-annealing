import numpy as np

# wybrać kilka z:
# https://en.wikipedia.org/wiki/Test_functions_for_optimization

def rastrigin_function(dimArray):
    sumPart = 0
    
    for x in dimArray:
        sumPart += (x ** 2 - 10 * np.cos(2 * np.pi * x))
        
    rastrigin = 10 * len(dimArray) + sumPart

    return rastrigin