from simulated_annealing_algorithm import *
from temperature_algorithms import *
from score_functions import *
import json
import os

# ################################################# #
#                                                   #        
#   Operować tylko parametrami w TESTS_PARAMETERS   #
#   Oraz nazwą funkcji celu w "RUN_TESTS"           #
#                                                   #
#   Wynik zapisuje się w folderze "results"         #
#   w pliku z nazwą funkcji celu, formacje json     #
#                                                   #
# ################################################# #


TESTS_PARAMETERS = {
    "repeat": 10,
    "max_iterations": 10000,
    "good_radius": 1.0,
    
    
    
    "score_functions": {
        "rastrigin": {
            "function":rastrigin_function,
            "clamp": 5.0,
            "startPoint": 5.0,
            "maximize": False,
            "global_minimum": 0
        }
    },
    "cooling": {
        "constant": {
            "function": constant,
            "a_paramater": [1] # nie ma znaczenia w tym chłodzeniu. Musi być 1 element, żeby poszła pętla. I tak nie wpływa na nic
        },
        "logarithmic": {
            "function": logarithmic,
            "a_paramater": [1, 2]
        },
        "exponential": {
            "function": exponential,
            "a_paramater": [1, 2]
        },
        "hyperbolic": {
            "function": hyperbolic,
            "a_paramater": [1, 2]
        },
    },
    "dimension": [1],
    "tabu_max_length": [0, 1, 5, 10],
    "temperature_max": [1, 5, 10, 50],
    "neighbour_radius": [2.0, 5.0],
    "tabu_radius": [0.5]     # oznacza mnożnik neighbour_radius przy przeszukiwaniu tabu => tabu_radius*neighbour_radius
}

def is_better_score(newScore, score, is_maximize):
    if (is_maximize):
        return newScore > newScore
    else:
        return newScore < score
        
        
def RUN_TEST():
    score_function_name = "rastrigin" # Tu zmienić nazwe optymalizowanej funkcji 
    
    result = test_one_function(score_function_name)        
    __save_json(score_function_name + ".json", result)    
    
        
def test_one_function(score_function_name):
    score_function_parameters = TESTS_PARAMETERS["score_functions"][score_function_name]
    score_function = score_function_parameters["function"]
    score_function_clamp = score_function_parameters["clamp"]
    score_function_startPoint = score_function_parameters["startPoint"]
    is_maximize_function = score_function_parameters["maximize"]
    
    result = {}
    result["score_function_name"] = score_function_name
    result["tests"] = []
    
    testsNum = __calcTestsNum(False)
    testsCounter = 1
    
    for cooling_function_name in TESTS_PARAMETERS["cooling"].keys():

        for cooling_A_param in TESTS_PARAMETERS["cooling"][cooling_function_name]["a_paramater"]:
        
            for dimensions in TESTS_PARAMETERS["dimension"]:
            
                for tabu_max_length in TESTS_PARAMETERS["tabu_max_length"]:
                    
                    for temperature_max in TESTS_PARAMETERS["temperature_max"]:
                    
                        for neighbour_radius in TESTS_PARAMETERS["neighbour_radius"]:
                            
                            for tabu_radius in TESTS_PARAMETERS["tabu_radius"]:
                                testResult = {}
                                options = {}
                                options["cooling_function_name"] = cooling_function_name
                                options["dimensions"] = dimensions
                                options["tabu_max_length"] = tabu_max_length
                                options["temperature_max"] = temperature_max
                                options["neighbour_radius"] = neighbour_radius
                                options["tabu_radius"] = tabu_radius
                                options["cooling_A_param"] = cooling_A_param
                                
                                testResult["options"] = options
                                
                                print("Test ", end="")
                                print(testsCounter, end="/")
                                print(testsNum, end=". ")
                                print(options)
                                print("Start...")
                                
                                
                                log = []
                                
                                for i in range(TESTS_PARAMETERS["repeat"]):
                                    algorithm_result = run_algorithm(score_function_name, 
                                                                    cooling_function_name,
                                                                    dimensions,
                                                                    tabu_max_length,
                                                                    temperature_max,
                                                                    neighbour_radius,
                                                                    tabu_radius,
                                                                    cooling_A_param)
                                                                    
                                    log.append(algorithm_result["best"])
                                
                                print("Test ", end="")
                                print(testsCounter, end="/")
                                print(testsNum, end=". ")
                                print("DONE", end='\n\n')
                                
                                testsCounter = testsCounter + 1
                                
                                testResult["result"] = __calcResult(log)
                                result["tests"].append(testResult)
                                
    return result
                
def run_algorithm(score_function_name, cooling_function_name, dimensions, tabu_max_length, temperature_max, neighbour_radius, tabu_radius, cooling_A_param):
    score_function_parameters = TESTS_PARAMETERS["score_functions"][score_function_name]
    score_function = score_function_parameters["function"]
    is_maximize_function = score_function_parameters["maximize"]
    cooling_function = TESTS_PARAMETERS["cooling"][cooling_function_name]["function"]
            
    
    start_point = [score_function_parameters["startPoint"] for i in range(dimensions)]
    simulated_annealing = SimulatedAnnealingAlgorithm(score_function, score_function_parameters["clamp"], is_maximize_function, tabu_max_length, neighbour_radius, tabu_radius)
    simulated_annealing.set_start_point(start_point)
    
    iteration = 0
    best_iteration = 0
    best_point = None
    temperature = temperature_max
    result = {}
    result["points"] = []
  
    if (is_maximize_function):
        best_score = -float('inf')
    else:
        best_score = float('inf')

    while (iteration < TESTS_PARAMETERS["max_iterations"]):
        iteration += 1
        
        if (cooling_function_name == "constant"):
            temperature = cooling_function(temperature)
        else:
            temperature = cooling_function(temperature, cooling_A_param, iteration)
        
        point, score = simulated_annealing.go(temperature) # point później do wykresów się przyda
        
        result["points"].append(point)
        
        if (is_better_score(score, best_score, is_maximize_function)):
            best_score = score
            best_iteration = iteration
            best_point = point
        
        if (score <= TESTS_PARAMETERS["good_radius"]):
            break

    result["best"] = {"best_point": best_point, "best_score": best_score, "best_score_iteration": best_iteration, "total_iteration": iteration}

    return result
    
    
def __save_json(file_name, data):

    file_name = "results\\" + file_name
    if not os.path.exists("results"):
        os.makedirs("results")
        
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print("Zapisano plik: ", end="")
    print(file_name)

    
    
def __calcResult(testResult):
    result = {}
    best_score_log = []
    for oneResult in testResult:
        best_score_log.append(oneResult["best_score"])
        
    result["min"] = np.min(best_score_log)
    result["max"] = np.max(best_score_log)
    result["mean"] = np.mean(best_score_log)
    
    return result
    
    
    
def __calcTestsNum(has_cooling_param = False):
    result = len(TESTS_PARAMETERS["dimension"])
    result = result * len(TESTS_PARAMETERS["tabu_max_length"])
    result = result * len(TESTS_PARAMETERS["temperature_max"])
    result = result * len(TESTS_PARAMETERS["neighbour_radius"])
    result = result * len(TESTS_PARAMETERS["tabu_radius"])
    
    coolingTests = 0
    
    for cooling in TESTS_PARAMETERS["cooling"].keys():
        coolingTests = coolingTests + len(TESTS_PARAMETERS["cooling"][cooling]["a_paramater"])
        
        
    result = result * coolingTests
    
    return result
    
   
   
