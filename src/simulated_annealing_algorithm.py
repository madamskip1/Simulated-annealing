import numpy as np
import random
import math

MIN_TEMPERATURE = 0.00000001 
MAX_TABU_TRIES = 50  # zabezpieczenie przed nieskończoną pętlą w generacji sąsiadów, która może wystąpić przy niektórych kombinacjach parametrów, Dzięki temu w skończonej liczbie prób zmienimy punkt

class SimulatedAnnealingAlgorithm:

    def __init__(self, score_function, cooling_function, cooling_param, temperature_init, clamp, is_maximize, tabu_max_length, neighbour_radius, tabu_radius):
        self._point = None
        self._score_func = score_function
        self._cooling_function = cooling_function
        self._cooling_param = cooling_param
        self._temperature = temperature_init
        self._score = -float('inf') if is_maximize else float('inf')
        self._clamp = clamp
        self._tabu = []
        self._tabu_max_length = tabu_max_length
        self._neighbour_radius = neighbour_radius
        self._tabu_radius =  tabu_radius * self._neighbour_radius # Dzięki temu nie będzie kombinacji, że tabu_radius > neighbour_radius
        self._is_maximize_function = is_maximize # jeśli fałsz to minimalizujemy, jak true to maksymalizujemy
    
    
    def run_one_iteration(self, iteration):
        new_point = self._generate_neighbour()
        score = self._score_func(new_point)

        self._calc_temperature(iteration)
        
        if (self._can_be_new_point(score)):
            self._point = new_point
            self._score = score
            
        self._tabu.append(self._point)
        self._try_delete_from_tabu()
        
        return self._point, self._score


    def set_start_point(self, point):
        self._point = point
        self._score = self._score_func(point)
 



    def _calc_temperature(self, iteration):
        self._temperature = self._cooling_function(self._temperature, self._cooling_param, iteration)
        if (self._temperature < MIN_TEMPERATURE):
            self._temperature = MIN_TEMPERATURE

    def _try_delete_from_tabu(self):
        if (len(self._tabu) > self._tabu_max_length):
            self._tabu.pop(0)
            
        
    def _generate_neighbour(self):
        triesCounter = 1
        
        while True:
            neighbourPoint = self._random_neighbour()
            
            if not self._check_if_tabu_neighbour(neighbourPoint):
                return neighbourPoint
                
            if (triesCounter >= MAX_TABU_TRIES): # zabezpieczenie przed nieskończoną pętlą, która może wystąpić przy niektórych kombinacjach parametrów, Dzięki temu w skończonej liczbie prób zmienimy punkt
                triesCounter = 0
                self._tabu.pop(0)
                
            triesCounter = triesCounter + 1
    
    
    def _random_neighbour(self):
        dim = len(self._point)
        
        neighbourPoint = np.random.uniform(-self._neighbour_radius, self._neighbour_radius, dim)
        neighbourPoint = neighbourPoint + self._point

        if (self._clamp != 0):
            neighbourPoint = neighbourPoint.clip(-self._clamp, self._clamp)

        return neighbourPoint
        
        
    def _check_if_tabu_neighbour(self, point):
        dim = len(point)
        
        for tabu_member in self._tabu:
            distance = np.linalg.norm(point - tabu_member)
            
            if (distance <= self._tabu_radius):
                return True
        
        return False
        
    
    def _can_be_new_point(self, score):
        if (self._is_maximize_function and score > self._score):
            return True
        elif (not self._is_maximize_function and score < self._score):
            return True
        elif (random.uniform(0, 1) < self._calc_pa(score)):
            return True
        else:
            return False
        
        
    def _calc_pa(self, score):
        return math.exp(-(abs(score - self._score) / self._temperature))