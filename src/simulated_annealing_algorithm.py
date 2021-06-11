import numpy as np
import random
import math

MIN_TEMPERATURE = 0.00000001 
MAX_TABU_TRIES = 50  # zabezpieczenie przed nieskończoną pętlą w generacji sąsiadów, która może wystąpić przy niektórych kombinacjach parametrów, Dzięki temu w skończonej liczbie prób zmienimy punkt

class SimulatedAnnealingAlgorithm:

    def __init__(self, score_function, clamp, is_maximize, tabu_max_length, neighbour_radius, tabu_radius):
        self._point = None
        self._score_func = score_function
        self._score = -float('inf') if is_maximize else float('inf')
        self._clamp = clamp
        self._tabu = []
        self._tabu_max_length = tabu_max_length
        self._neighbour_radius = neighbour_radius
        self._tabu_radius =  tabu_radius * self._neighbour_radius # Dzięki temu nie będzie kombinacji, że tabu_radius > neighbour_radius
        self._is_maximize_function = is_maximize # jeśli fałsz to minimalizujemy, jak true to maksymalizujemy
    
    
    def go(self, temperature):
        new_point = self._generate_neighbour()
        score = self._score_func(new_point)

        if (self._can_be_new_point(score, temperature)):
            self._point = new_point
            self._score = score
            
        self._tabu.append(self._point)
        self._try_delete_from_tabu()
        
        return self._point, self._score


    def set_start_point(self, point):
        self._point = point
        self._score = self._score_func(point)
        
    
    def getScore(self):
        return self._score



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
        
    
    def _can_be_new_point(self, score, temperature):
        if (self._is_maximize_function and score > self._score):
            return True
        elif (not self._is_maximize_function and score < self._score):
            return True
        elif (random.uniform(0, 1) < self._calc_pa(temperature, score)):
            return True
        else:
            return False
        
        
    def _calc_pa(self, temperature, score):
        if (temperature < MIN_TEMPERATURE):
            temperature = MIN_TEMPERATURE
        
        return math.exp(-(abs(score - self._score) / temperature))