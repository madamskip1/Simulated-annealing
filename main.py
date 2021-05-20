from simulated_annealing_algorithm import *
from temperature_algorithms import *
from score_functions import *

# napisać funkcje testowa, która będzie wywoływać z kolejnymi parametrami i róznymi algorytmami chłodzenia


TABU_MAX_LENGTH = 10
MAX_ITERATIONS = 10000
T_MAX = 10
GOOD_RADIUS = 0.1 # promień od optimum globalnego uznawany za wystarczający
DIM = 2

TESTS_PARAMETERS = {
    "repeat": 10,
    "dimensions": [1, 2, 5, 10, 20],
    "score_functions": {
        "rastrigin": {
            "function":rastrigin_function,
            "clamp": 5.0,
            "startPoint": 5.0,
        }
    },
    "cooling": {
        "constant": constant,
        "logarithimic": logarithimic,
        "exponential": exponential,
        "hyperbolic": hyperbolic
    }
    "cooling_A_param": [1, 10, 50, 10, 500, 1000],
    "tabu_max_length": [0, 1, 5, 10, 20, 50],
    "max_iterations": 10000,
    "temperature_max": [1, 5, 10, 20, 50, 100],
    "good_radius": 1.0
}

def main():
    point = np.random.uniform(0, 5.0, DIM)
    point = point.clip(-5.0, 5.0)
    simulated_annealing = SimulatedAnnealingAlgorithm(rastrigin_function, 5.0)
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