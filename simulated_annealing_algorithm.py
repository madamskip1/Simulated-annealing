import numpy as np
import random
import math

TABU_MAX_LENGTH = 10
# napisać funkcje generacji sąsiadów

class SimulatedAnnealingAlgorithm:

    def __init__(self, score_function, clamp = 0.0):
        #trzeba poustawiac wybrane parametry
        # najlepiej w konstruktorze lub przez metode
        # wtedy łatwiej będzie testować
        # TO DO
        self._point = None
        self._score_func = score_function
        self._score = 0
        self._clamp = clamp;
        self._tabu = []
        self._tabu_max_length = TABU_MAX_LENGTH
        self._neighbour_radius = 10
        self._tabu_radius = 3
        self._is_maximize_function = False # jeśli fałsz to minimalizujemy, jak true to maksymalizujemy
    
    def set_start_point(self, point):
        self._point = point
        self._score = self._score_func(point)
        
        
    def go(self, temperature):
        new_point = self._generate_neighbour()

        score = self._score_func(new_point)
    
        if (self._can_be_new_point(score, temperature)):
            self._point = new_point
            self._score = score
            
        self._tabu.append(self._point)
        
        self._try_delete_from_tabu()
        
        return self._score
    
    def getScore(self):
        return self._score
        
    
    def _try_delete_from_tabu(self):
        if (len(self._tabu) > self._tabu_max_length):
            self._tabu.pop(0)
        
    def _generate_neighbour(self):
    # funkcja generuje kolejnych sąsiadów, aż znajdzie takiego, który może być użyty
        while True:
            neighbourPoint = self._random_neighbour()
            
            if not self._check_if_tabu_neighbour(neighbourPoint):
                return neighbourPoint
    
    def _random_neighbour(self):
    # funkcja zwraca losowego sąsiada aktualnego punktu
    # TRZEBA ZROBIĆ LEPSZĄ !!!!
        dim = len(self._point)
        
        neighbourPoint = np.random.uniform(-self._neighbour_radius, self._neighbour_radius, dim)
        neighbourPoint = neighbourPoint + self._point

        if (self._clamp != 0):
            neighbourPoint = neighbourPoint.clip(-self._clamp, self._clamp)

        return neighbourPoint
        
    def _check_if_tabu_neighbour(self, point):
    # funkcja sprawdzajaca czy punkt lezy w sasiedztwie jakiegos punktu w tab_radius
        dim = len(point)

        for x in range(dim):
            temp = abs(point[x] - self._point[x])
            
            if (temp <= self._tabu_radius):
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
        return math.exp(-(abs(score - self._score)) / temperature)
        
        