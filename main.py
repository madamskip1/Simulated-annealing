from simulated_annealing_algorithm import *
from temperature_algorithms import *
from score_functions import *

# napisać funkcje testowa, która będzie wywoływać z kolejnymi parametrami i róznymi algorytmami chłodzenia


TABU_MAX_LENGTH = 10
MAX_ITERATIONS = 10000
T_MAX = 5
GOOD_RADIUS = 0.01 # promień od optimum globalnego uznawany za wystarczający
DIM = 4

def main():
    point = np.random.uniform(0, 100, DIM)
    simulated_annealing = SimulatedAnnealingAlgorithm(rastrigin_function)
    simulated_annealing.set_start_point(point)
    
    iteration = 0
    temp = T_MAX

    while (iteration < MAX_ITERATIONS):
        temperature = constant(temp) # tu można zmieniać algorytm chłodzenia
        score = simulated_annealing.go(temp)

        print(iteration, end=": ")
        print(simulated_annealing.getScore())
        
        if (score <= GOOD_RADIUS):
            return iteration
            
        iteration += 1
    
    
main()