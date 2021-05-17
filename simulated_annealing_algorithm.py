import numpy as np
import random
import math

# napisać funkcje generacji sąsiadów

class SimulatedAnnealingAlgorithm;

    def __init__(self):
        #trzeba poustawiac wybrane parametry
        # najlepiej w konstruktorze lub przez metode
        # wtedy łatwiej będzie testować
        # TO DO
        _point = None
        _score_func = None
        _score = 0
        _tabu = []
        _tabu_max_length = tabu_max_length
        _neighbour_radius = 0
        _tabu_radius = 0 
    
    def go(self, temp):
        new_point = self._generate_neighbour()
        score = _self._score_func(new_point)
        
        if (self._can_be_new_point(score, temp)):
            self._point = new_point
            self._score = score
            
        self._tabu.append(self._point)
        
        if (len(self._tabu) > self._tabu_max_length):
            self._tabu.pop(0)
        
        
    def _generate_neighbour(self):
    # funkcja generuje kolejnych sąsiadów, aż znajdzie takiego, który może być użyty
        while True:
            neighbourPoint = self._random_neighbour()
            
            if not _check_if_tabu_neighbour(neighbourPoint)
                return neighbourPoint
    
    def _random_neighbour(self):
    # funkcja zwraca losowego sąsiada aktualnego punktu
    # MOŻE TRZEBA ZROBIC INNA
        dim = len(self._point)
        neighbourPoint = np.random.uniform(-self._neighbour_radius, self._neighbour_radius, dim)
        neighbourPoint = neighbourPoint + self._point
        
        return neighbourPoint
        
    def _check_if_tabu_neighbour(self, point):
    # funkcja sprawdzajaca czy punkt lezy w sasiedztwie jakiegos punktu w tabu_max_length
        dim = len(point)
        for x in range(dim):
            temp = point[x] - self._point[x]
            if (temp <= self._tabu_radius)
                return true
        
        return false
        
    
    def _can_be_new_point(self, score, temp):
        if (score > self._score):
            return true
        elif (random.uniform(0, 1) < self._calc_pa(temp, score)):
            return true
        else:
            return false
        
    def _calc_pa(temp, score):
        return exp(-(abs(score - self._score)) / temp)
        
        