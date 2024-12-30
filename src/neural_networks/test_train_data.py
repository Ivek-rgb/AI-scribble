
import random

class Point:
    
    def __init__(self): 
        self.pointX = random.uniform(-100, 100)
        self.pointY = random.uniform(-100, 100)
        self.result = 1 if self.pointY > self.pointX else 0 if self.pointY == self.pointX else -1 
        self.bias = 1
        