from main import run_algorithm, TESTS_PARAMETERS
import numpy as np
import matplotlib.pyplot as plt
import os


# #################################
# USTAWIENIA
score_function_name = "rastrigin"
cooling_function_name = "constant"
cooling_A_param = 0

tabu_max_length = 5
temperature_init = 50
neighbour_radius = 1.0
tabu_radius = 0.5

plot_num = -1 # opcjonalnie, jeśli chcemy kolejne z tymi samymi ustawieniami, żeby były zapisane pod inną nazwą. Wartość -1 jest pomijana w nazwie


# KONIEC USTAWIEN
# ###############################






Colors = {
        'global_optimum': '#FF0000',
        'best_point': '#00FF00'
        }


title = score_function_name + "_" + cooling_function_name + "_" + str(cooling_A_param)
if plot_num != -1:
    title = title + "_ID" + str(plot_num)



test = run_algorithm(score_function_name, cooling_function_name, 2, tabu_max_length, temperature_init, neighbour_radius, tabu_radius, cooling_A_param)

x = []
y = []

for point in test["points"]:
    x.append(point[0])
    y.append(point[1])


plt.scatter(x, y)
global_optimum_point = TESTS_PARAMETERS["score_functions"][score_function_name]["global_optimum"]
plt.plot(global_optimum_point[0], global_optimum_point[1], color=Colors['global_optimum'], marker='o')
plt.plot(test["best"]["best_point"][0], test["best"]["best_point"][1], color=Colors['best_point'], marker='o')
plt.grid(True)

axisLim = TESTS_PARAMETERS["score_functions"][score_function_name]["clamp"]
axisLim = axisLim * 1.1
plt.xlim([-axisLim, axisLim])
plt.ylim([-axisLim, axisLim])

plt.title(title)

if not os.path.exists("plot_images"):
    os.makedirs("plot_images")
    
plt.savefig('plot_images\\' + title + '.png')
plt.show()