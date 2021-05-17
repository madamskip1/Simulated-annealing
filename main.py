from simulated_annealing_algorithm import *
from temperature_algorithms import *

# napisać funkcje testowa, która będzie wywoływać z kolejnymi parametrami i róznymi algorytmami chłodzenia


TABU_MAX_LENGTH = 10
MAX_ITERATIONS = 10000
T_MAX = 100
GOOD_RADIUS = 0.01 # promień od optimum globalnego uznawany za wystarczający

def main():
    simulated_annealing = (TABU_MAX_LENGTH)
    
    iteration = 0
    temp = T_MAX
    
    while (iteration < MAX_ITERATION):
        temperature = constant(temp) # tu można zmieniać algorytm chłodzenia
        
        point = simulated_annealing.go(temp)
        
        if (point <= GOOD_RADIUS)
            return iteration
    