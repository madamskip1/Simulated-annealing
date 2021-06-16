from main import run_algorithm, TESTS_PARAMETERS
import numpy as np
import matplotlib.pyplot as plt
import os
import json

# #################################
# USTAWIENIA


params = [
    {
        "score_function_name": "rastrigin",
        "cooling_function_name": "logarithmic",
        "tabu_max_length": 50,
        "temperature_init": 100,
        "neighbour_radius": 1.0,
        "tabu_radius": 0.001,
        "cooling_A_param": 0.001,

        "plot_num": -1,
    },
    {
        "score_function_name": "rastrigin",
        "cooling_function_name": "exponential",
        "tabu_max_length": 0,
        "temperature_init": 10000,
        "neighbour_radius": 1.0,
        "tabu_radius": 0.001,
        "cooling_A_param": 0.5,

        "plot_num": -1,
    },
    {
        "score_function_name": "rastrigin",
        "cooling_function_name": "hyperbolic",
        "tabu_max_length": 50,
        "temperature_init": 100,
        "neighbour_radius": 1.0,
        "tabu_radius": 0.001,
        "cooling_A_param": 0.001,

        "plot_num": -1,
    },
    {
        "score_function_name": "rastrigin",
        "cooling_function_name": "constant",
        "tabu_max_length": 0,
        "temperature_init": 1,
        "neighbour_radius": 1.0,
        "tabu_radius": 0.001,
        "cooling_A_param": 1,

        "plot_num": -1,
    },
    {
        "score_function_name": "rosenbrock",
        "cooling_function_name": "logarithmic",
        "tabu_max_length": 50,
        "temperature_init": 1,
        "neighbour_radius": 1.0,
        "tabu_radius": 0.001,
        "cooling_A_param": 0.001,

        "plot_num": -1,
    },
    {
        "score_function_name": "rosenbrock",
        "cooling_function_name": "exponential",
        "tabu_max_length": 10,
        "temperature_init": 1000,
        "neighbour_radius": 1.0,
        "tabu_radius": 0.001,
        "cooling_A_param": 0.5,

        "plot_num": -1,
    },
    {
        "score_function_name": "rosenbrock",
        "cooling_function_name": "hyperbolic",
        "tabu_max_length": 0,
        "temperature_init": 100,
        "neighbour_radius": 1.0,
        "tabu_radius": 0.001,
        "cooling_A_param": 0.01,

        "plot_num": -1,
    },
    {
        "score_function_name": "rosenbrock",
        "cooling_function_name": "constant",
        "tabu_max_length": 10,
        "temperature_init": 1,
        "neighbour_radius": 1.0,
        "tabu_radius": 0.001,
        "cooling_A_param": 1,

        "plot_num": -1,
    },
    {
        "score_function_name": "ackley",
        "cooling_function_name": "logarithmic",
        "tabu_max_length": 10,
        "temperature_init": 1,
        "neighbour_radius": 1.0,
        "tabu_radius": 0.001,
        "cooling_A_param": 0.01,

        "plot_num": -1,
    },
    {
        "score_function_name": "ackley",
        "cooling_function_name": "exponential",
        "tabu_max_length": 0,
        "temperature_init": 10000,
        "neighbour_radius": 1.0,
        "tabu_radius": 0.001,
        "cooling_A_param": 0.5,

        "plot_num": -1,
    },
    {
        "score_function_name": "ackley",
        "cooling_function_name": "hyperbolic",
        "tabu_max_length": 10,
        "temperature_init": 10000,
        "neighbour_radius": 1,
        "tabu_radius": 0.001,
        "cooling_A_param": 0.001,

        "plot_num": -1,
    },
    {
        "score_function_name": "ackley",
        "cooling_function_name": "constant",
        "tabu_max_length": 0,
        "temperature_init": 1,
        "neighbour_radius": 0.1,
        "tabu_radius": 0.001,
        "cooling_A_param": 1,

        "plot_num": -1,
    },
    {
        "score_function_name": "levi_n13",
        "cooling_function_name": "logarithmic",
        "tabu_max_length": 50,
        "temperature_init": 10000,
        "neighbour_radius": 2.0,
        "tabu_radius": 0.001,
        "cooling_A_param": 0.01,

        "plot_num": -1,
    },
    {
        "score_function_name": "levi_n13",
        "cooling_function_name": "exponential",
        "tabu_max_length": 10,
        "temperature_init": 1,
        "neighbour_radius": 2.0,
        "tabu_radius": 0.001,
        "cooling_A_param": 0.1,

        "plot_num": -1,
    },
    {
        "score_function_name": "levi_n13",
        "cooling_function_name": "hyperbolic",
        "tabu_max_length": 50,
        "temperature_init": 10000,
        "neighbour_radius": 2.0,
        "tabu_radius": 0.001,
        "cooling_A_param": 0.001,

        "plot_num": -1,
    },
    {
        "score_function_name": "levi_n13",
        "cooling_function_name": "constant",
        "tabu_max_length": 50,
        "temperature_init": 1,
        "neighbour_radius": 2.0,
        "tabu_radius": 0.001,
        "cooling_A_param": 1,

        "plot_num": -1,
    }
]


score_plot_step =10 # co ktora iteracja ma byc zapisywana na wykresie wartości funkcji

# KONIEC USTAWIEN
# ###############################






Colors = {
        'global_optimum': '#FF0000',
        'best_point': '#00FF00'
        }
        
testNum = len(params)
testCounter = 1

for testId in range(len(params)):
    print("Test ", end='')
    print(testCounter, end="/")
    print(testNum, end=": ")
    print("Start")
    
    test_param = params[testId]
    
    score_function_name = test_param["score_function_name"]
    cooling_function_name = test_param["cooling_function_name"]
    cooling_A_param = test_param["cooling_A_param"]

    tabu_max_length = test_param["tabu_max_length"]
    temperature_init = test_param["temperature_init"]
    neighbour_radius = test_param["neighbour_radius"]
    tabu_radius = test_param["tabu_radius"]

    plot_num = test_param["plot_num"]
    
    
    title = score_function_name + "_" + cooling_function_name + "_" + str(cooling_A_param) + "_" + str(tabu_max_length) + "_" + str(temperature_init) + "_" + str (neighbour_radius) + "_" + str(tabu_radius)
    if plot_num != -1:
        title = title + "_ID" + str(plot_num)



    algorithm_result = run_algorithm(score_function_name, cooling_function_name, 2, tabu_max_length, temperature_init, neighbour_radius, tabu_radius, cooling_A_param)


    # make point plot
    x = []
    y = []

    for point in algorithm_result["points"]:
        x.append(point[0])
        y.append(point[1])

    plt.clf()

    plt.scatter(x, y, s=1)
    global_optimum_point = TESTS_PARAMETERS["score_functions"][score_function_name]["global_optimum"]
    plt.plot(global_optimum_point[0], global_optimum_point[1], color=Colors['global_optimum'], marker='o')
    plt.plot(algorithm_result["best"]["best_point"][0], algorithm_result["best"]["best_point"][1], color=Colors['best_point'], marker='o')
    plt.grid(True)

    axisLim = TESTS_PARAMETERS["score_functions"][score_function_name]["clamp"]
    axisLim = axisLim * 1.1
    plt.xlim([-axisLim, axisLim])
    plt.ylim([-axisLim, axisLim])

    plt.title(title)

    # save point plot 
    dirPointPlot = "../point_plot/"
    
    if not os.path.exists(dirPointPlot):
        os.makedirs(dirPointPlot)
        
    plt.savefig(dirPointPlot + title + '.png')
    print("Point plot saved...")
    
    # make score plot
    score_plot_log_Y = []
    score_plot_log_X = []
    
    for pointID in range(0, len(algorithm_result["scores"]), score_plot_step):
        score_plot_log_X.append(pointID)
        score_plot_log_Y.append(algorithm_result["scores"][pointID])
    
    plt.clf()
    plt.plot(score_plot_log_X, score_plot_log_Y)
    
    # save score plot

    dirScorePlot = "../score_plot/"

    if not os.path.exists(dirScorePlot):
        os.makedirs(dirScorePlot)

    plt.savefig(dirScorePlot + title + '.png')
    print("Score plot saved...")
    
    print("Test ", end='')
    print(testCounter, end="/")
    print(testNum, end=": ")
    print("Done", end='\n\n')
    
    testCounter = testCounter + 1