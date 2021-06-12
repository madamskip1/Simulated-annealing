from main import run_algorithm, TESTS_PARAMETERS
import numpy as np
import matplotlib.pyplot as plt
import os
import json

# #################################
# USTAWIENIA
score_function_name = "ackley"
cooling_function_name = "constant"
cooling_A_param = 1

tabu_max_length = 0
temperature_init = 1
neighbour_radius = 0.1
tabu_radius = 0.001

csv_num = -1 # opcjonalnie, jeśli chcemy kolejne z tymi samymi ustawieniami, żeby były zapisane pod inną nazwą. Wartość -1 jest pomijana w nazwie

csv_step = 5 # co która iteracje ma zapisać do csv (1 = każdą, 5 = co piątą itd)

# KONIEC USTAWIEN
# ###############################



title = score_function_name + "_" + cooling_function_name + "_" + str(cooling_A_param)

if csv_num != -1:
    title = title + "_ID" + str(csv_num)



result = run_algorithm(score_function_name, cooling_function_name, 2, tabu_max_length, temperature_init, neighbour_radius, tabu_radius, cooling_A_param)

csvResult = []

for i in range(0, len(result["scores"]), csv_step):
    csvResult.append([i, result["scores"][i]])



dirCSV = "../csv_results/"

if not os.path.exists(dirCSV):
    os.makedirs(dirCSV)

np.savetxt(dirCSV + title + ".csv", csvResult, delimiter=',', header="point_num,score", comments='')