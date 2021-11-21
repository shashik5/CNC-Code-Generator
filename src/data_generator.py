from numpy import random, column_stack

class DataGenerator:
    def __init__(self, width, height, nodesNumber):
        self.width = width
        self.height = height
        self.nodesNumber = nodesNumber

    def generate(self):
        xs = random.randint(self.width, size=self.nodesNumber)
        ys = random.randint(self.height, size=self.nodesNumber)
        return column_stack((xs, ys))
