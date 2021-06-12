from main import run_algorithm, TESTS_PARAMETERS
import numpy as np
import matplotlib.pyplot as plt
import os


# #################################
# USTAWIENIA


params = [

    {
        "score_function_name": "ackley",
        "cooling_function_name": "constant",
        "cooling_A_param": 1,
        "tabu_max_length": 0,
        "temperature_init": 1,
        "neighbour_radius": 0.1,
        "tabu_radius": 0.001,
        "plot_num": -1,
    },
        {
        "score_function_name": "ackley",
        "cooling_function_name": "logarithmic",
        "cooling_A_param": 1,
        "tabu_max_length": 100,
        "temperature_init": 1,
        "neighbour_radius": 0.1,
        "tabu_radius": 0.001,
        "plot_num": -1,
    },
]

# KONIEC USTAWIEN
# ###############################






Colors = {
        'global_optimum': '#FF0000',
        'best_point': '#00FF00'
        }

for testId in range(len(params)):
    test_param = params[testId]
    
    score_function_name = test_param["score_function_name"]
    cooling_function_name = test_param["cooling_function_name"]
    cooling_A_param = test_param["cooling_A_param"]

    tabu_max_length = test_param["tabu_max_length"]
    temperature_init = test_param["temperature_init"]
    neighbour_radius = test_param["neighbour_radius"]
    tabu_radius = test_param["tabu_radius"]

    plot_num = test_param["plot_num"]
    
    
    title = score_function_name + "_" + cooling_function_name + "_" + str(cooling_A_param) + str(tabu_max_length) + str(temperature_init) + str (neighbour_radius) + str(tabu_radius)
    if plot_num != -1:
        title = title + "_ID" + str(plot_num)



    test = run_algorithm(score_function_name, cooling_function_name, 2, tabu_max_length, temperature_init, neighbour_radius, tabu_radius, cooling_A_param)

    x = []
    y = []

    for point in test["points"]:
        x.append(point[0])
        y.append(point[1])

    plt.clf()

    plt.scatter(x, y, s=1)
    global_optimum_point = TESTS_PARAMETERS["score_functions"][score_function_name]["global_optimum"]
    plt.plot(global_optimum_point[0], global_optimum_point[1], color=Colors['global_optimum'], marker='o')
    plt.plot(test["best"]["best_point"][0], test["best"]["best_point"][1], color=Colors['best_point'], marker='o')
    plt.grid(True)

    axisLim = TESTS_PARAMETERS["score_functions"][score_function_name]["clamp"]
    axisLim = axisLim * 1.1
    plt.xlim([-axisLim, axisLim])
    plt.ylim([-axisLim, axisLim])

    plt.title(title)

    dirPlotImages = "../plot_images/"

    if not os.path.exists(dirPlotImages):
        os.makedirs(dirPlotImages)
        
    plt.savefig(dirPlotImages + title + '.png')