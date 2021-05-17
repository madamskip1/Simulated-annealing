import numpy as np
import random
import math

# napisać funkcje generacji sąsiadów

class SimulatedAnnealingAlgorithm;

    def __init__(self, tabu_max_length):
        _point = None
        _score_func = None
        _score = 0
        _tabu = []
        _tabu_max_length = tabu_max_length
    
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
    # ta funkcja bedzie zwracac prawidlowego sasiada
    # wywola funkcje _random_neighbour
    
    def _random_neighbour(self):
    # ta funkcja będzie zwracać losowego sasiada
    # wywolywana w _generate_neighbour
    
    def _can_be_new_point(self, score, temp):
        if (score > self._score):
            return true
        elif (random.uniform(0, 1) < self._calc_pa(temp, score)):
            return true
        else:
            return false
        
    def _calc_pa(temp, score):
        return exp(-(abs(score - self._score)) / temp)
        
        