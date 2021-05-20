from simulated_annealing_algorithm import *
from temperature_algorithms import *
from score_functions import *

# napisać funkcje testowa, która będzie wywoływać z kolejnymi parametrami i róznymi algorytmami chłodzenia


TABU_MAX_LENGTH = 10
GOOD_RADIUS = 0.1 # promień od optimum globalnego uznawany za wystarczający
DIM = 2

TESTS_PARAMETERS = {
    "repeat": 10,
    "max_iterations": 1000,
    
    
    "dimension": [1, 2, 5, 10, 20],
    "score_functions": {
        "rastrigin": {
            "function":rastrigin_function,
            "clamp": 5.0,
            "startPoint": 5.0,
            "maximize": False
        }
    },
    "cooling": {
        "constant": constant,
        "logarithmic": logarithmic,
        "exponential": exponential,
        "hyperbolic": hyperbolic
    },
    "cooling_A_param": [1, 10, 50, 10, 500, 1000],
    "tabu_max_length": [0, 1, 5, 10, 20, 50],
    "temperature_max": [1, 5, 10, 20, 50, 100],
    "good_radius": 1.0,
    "neighbour_radius": [0.1, 0.2, 0.5, 1.0, 2.0, 5.0],
    "tabu_radius": [0.1, 0.25, 0.5]     # oznacza mnożnik neighbour_radius przy przeszukiwaniu tabu => tabu_radius*neighbour_radius
}

def is_better_score(newScore, score, is_maximize):
    if (is_maximize):
        return newScore > newScore
    else:
        return newScore < score

def main():
    # ######## PARAMETRY TESTU ###############
    
    # te ustawiamy:
    # (później można to zrobić pętlami, żeby wybierało z TESTS_PARAMETERS i odpalało samo. Odpala się i idzie spać - same będą się robiły)
    score_function_name = "rastrigin"
    cooling_function_name = "constant"
    cooling_A_parameter = TESTS_PARAMETERS["cooling_A_param"][0]
    dimension = TESTS_PARAMETERS["dimension"][2]
    temperature_max = TESTS_PARAMETERS["temperature_max"][2]
    neighbour_radius = TESTS_PARAMETERS["neighbour_radius"][3]
    tabu_max_length = TESTS_PARAMETERS["tabu_max_length"][2]
    neighbour_radius = TESTS_PARAMETERS["neighbour_radius"][3]
    tabu_radius = TESTS_PARAMETERS["tabu_radius"][1]
    
    # tych już nie dotykamy
    cooling_function = TESTS_PARAMETERS["cooling"][cooling_function_name]
    score_function = TESTS_PARAMETERS["score_functions"][score_function_name]
    is_maximize_function = score_function["maximize"]
    # #########################################
    
    results = []
    
    for i in range(TESTS_PARAMETERS["repeat"]):
        start_point = [score_function["startPoint"] for i in range(dimension)]
        simulated_annealing = SimulatedAnnealingAlgorithm(score_function["function"], score_function["clamp"], is_maximize_function, tabu_max_length, neighbour_radius, tabu_radius)
        simulated_annealing.set_start_point(start_point)
        
        iteration = 0
        best_iteration = 0
        best_point = None
        temperature = temperature_max
        
        if (is_maximize_function):
            best_score = -float('inf')
        else:
            best_score = float('inf')

        while (iteration < TESTS_PARAMETERS["max_iterations"]):
            iteration += 1
            
            if (cooling_function_name == "constant"):
                temperature = cooling_function(temperature)
            else:
                temperature = cooling_function(temperature, cooling_A_parameter, iteration)
            
            
            point, score = simulated_annealing.go(temperature) # point później do wykresów się przyda
            
            if (is_better_score(score, best_score, is_maximize_function)):
                best_score = score
                best_iteration = iteration
                best_point = point

            
            if (score <= GOOD_RADIUS):
                break
                
            
        
        print("Best score: ", end="")
        print(best_score, end="")
        print(", in: ", end="")
        print(best_iteration, end="")
        print(" iteration.", end="")
        print(" Total iterations: ", end="")
        print(iteration)
        
        results.append({"best_point": best_point, "best_score": best_score, "best_score_iteration": best_iteration, "total_iteration": iteration})

    return results
    
main()