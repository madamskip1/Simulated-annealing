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
    "max_iterations": 10000, # musi być dużo więcej 5-10tyś +
    "good_score": 1.0, # kiedy uznajemy, że wynik jest wystarczający
                        # dla minimalizacji score <= good_score
                        # dla maksymalizacji score >= good_score
    
    
    
    "score_functions": {
        "rastrigin": {
            "function":rastrigin_function,
            "clamp": 5.12,          # przedzial w ktorym funkcja jest okreslona
            "startPoint": 5.0,      # punkt startowy (każdy wymiar będzie miał tę wartość - pozwala powtarzać testy z tego samego punktu
            "maximize": False,      # czy funkcje minimalizujemy czy maksymalizujemy
            "global_optimum": [0, 0]     # do rysowania grafów. 
        }
    },
    "cooling": {
        "constant": {
            "function": constant,
            "a_paramater": [1] # nie ma znaczenia w tym chłodzeniu. Musi być 1 element, żeby poszła pętla. I tak nie wpływa na nic
        },
        "logarithmic": {
            "function": logarithmic,
            "a_paramater": [0.001, 0.0005] # im mniejszy tym temperatura spada wolniej
        },
        "exponential": {
            "function": exponential,
            "a_paramater": [0.9, 1/2] # w wykładniczej parametr musi być <1
        },
        "hyperbolic": {
            "function": hyperbolic,
            "a_paramater": [0.001, 0.0005] # im mniejszy tym temperatura spada wolniej
        },
    },
    "dimension": [2],
    "tabu_max_length": [0, 1, 5, 10],
    "temperature_init": [0.1, 1, 10, 50],
    "neighbour_radius": [0.5, 1.0],
    "tabu_radius": [0.5]     # oznacza mnożnik neighbour_radius przy przeszukiwaniu tabu => tabu_radius*neighbour_radius. Dzięki temu nie będzie kombinacji, że tabu_radius > neighbour_radius
}
        
def RUN_TEST():
    score_function_name = "rastrigin" # Tu ustawiamy jaka funkcja bedzie optymalizowana!!!!!!!!!!!!!!
    
    result = __test_one_function(score_function_name)        
    __save_json(score_function_name + ".json", result)    
    









        
def __test_one_function(score_function_name):
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
                    
                    for temperature_init in TESTS_PARAMETERS["temperature_init"]:
                    
                        for neighbour_radius in TESTS_PARAMETERS["neighbour_radius"]:
                            
                            for tabu_radius in TESTS_PARAMETERS["tabu_radius"]:
                                testResult = {}
                                options = {}
                                options["cooling_function_name"] = cooling_function_name
                                options["dimensions"] = dimensions
                                options["tabu_max_length"] = tabu_max_length
                                options["temperature_init"] = temperature_init
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
                                                                    temperature_init,
                                                                    neighbour_radius,
                                                                    tabu_radius,
                                                                    cooling_A_param)
                                                                    
                                    log.append(algorithm_result["best"])
                                
                                print("Test ", end="")
                                print(testsCounter, end="/")
                                print(testsNum, end=". ")
                                print("DONE", end='\n\n')
                                
                                testsCounter = testsCounter + 1
                                
                                testResult["result"] = __calcTestResult(log)
                                result["tests"].append(testResult)
                                
                                __save_json(score_function_name + "_temp.json", result) # zapisanie po każdym teście zabezpiecza przed utratą danych, jeśli któraś kombinacja parametrów się zatnie
                                
    return result
                
def run_algorithm(score_function_name, cooling_function_name, dimensions, tabu_max_length, temperature_init, neighbour_radius, tabu_radius, cooling_A_param):
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
    temperature = temperature_init
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
        
        point, score = simulated_annealing.go(temperature)
        
        result["points"].append(point)
        
        if (__is_better_score(score, best_score, is_maximize_function)):
            best_score = score
            best_iteration = iteration
            best_point = point
        
        if (not is_maximize_function and score <= TESTS_PARAMETERS["good_score"]):
            break
        elif (is_maximize_function and score >= TESTS_PARAMETERS["good_score"]):
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



def __is_better_score(newScore, score, is_maximize):
    if (is_maximize):
        return newScore > newScore
    else:
        return newScore < score
        
    
def __calcTestResult(testResult):
    result = {}
    best_score_log = []
    total_iteration_log = []
    best_score_iteration_log = []
    
    for oneResult in testResult:
        best_score_log.append(oneResult["best_score"])
        total_iteration_log.append(oneResult["total_iteration"])
        best_score_iteration_log.append(oneResult["best_score_iteration"])
        
    result["min"] = np.min(best_score_log).item()
    result["max"] = np.max(best_score_log).item()
    result["mean"] = np.mean(best_score_log).item()
    result["best_score_iteration_mean"] = np.mean(best_score_iteration_log).item()
    result["best_score_iteration_min"] = np.min(best_score_iteration_log).item()
    result["total_iteration_min"] = np.min(total_iteration_log).item()
    result["total_iteration_mean"] = np.mean(total_iteration_log).item()
    

    return result
    
    
    
def __calcTestsNum(has_cooling_param = False):
    result = len(TESTS_PARAMETERS["dimension"])
    result = result * len(TESTS_PARAMETERS["tabu_max_length"])
    result = result * len(TESTS_PARAMETERS["temperature_init"])
    result = result * len(TESTS_PARAMETERS["neighbour_radius"])
    result = result * len(TESTS_PARAMETERS["tabu_radius"])
    
    coolingTests = 0
    
    for cooling in TESTS_PARAMETERS["cooling"].keys():
        coolingTests = coolingTests + len(TESTS_PARAMETERS["cooling"][cooling]["a_paramater"])
        
        
    result = result * coolingTests
    
    return result