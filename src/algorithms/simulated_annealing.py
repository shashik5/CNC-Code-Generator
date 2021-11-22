import math
import random
import utils


class SimulatedAnnealingConfig:
    def __init__(self, temp: int, stoppingTemp: float, alpha: float, stoppingIter: float) -> None:
        self.temp = temp
        self.stoppingTemp = stoppingTemp
        self.alpha = alpha
        self.stoppingIter = stoppingIter


class SimulatedAnnealing:
    def __init__(self, coords, config: SimulatedAnnealingConfig):
        self.coords = coords
        self.sample_size = len(coords)
        self.temp = config.temp
        self.alpha = config.alpha
        self.stopping_temp = config.stoppingTemp
        self.stopping_iter = config.stoppingIter
        self.iteration = 1

        self.dist_matrix = utils.vectorToDistMatrix(coords)
        self.curr_solution = utils.nearestNeighbourSolution(self.dist_matrix)
        self.best_solution = self.curr_solution

        self.solutionHistory = [self.curr_solution]

        self.curr_weight = self.weight(self.curr_solution)
        self.initial_weight = self.curr_weight
        self.min_weight = self.curr_weight

        self.weight_list = [self.curr_weight]

        print('Intial weight: ', self.curr_weight)

    def weight(self, sol):
        return sum([self.dist_matrix[i, j] for i, j in zip(sol, sol[1:] + [sol[0]])])

    def acceptance_probability(self, candidate_weight):
        '''
        Acceptance probability as described in:
        https://stackoverflow.com/questions/19757551/basics-of-simulated-annealing-in-python
        '''
        return math.exp(-abs(candidate_weight - self.curr_weight) / self.temp)

    def accept(self, candidate):
        '''
        Accept with probability 1 if candidate solution is better than
        current solution, else accept with probability equal to the
        acceptance_probability()
        '''
        candidate_weight = self.weight(candidate)
        if candidate_weight < self.curr_weight:
            self.curr_weight = candidate_weight
            self.curr_solution = candidate
            if candidate_weight < self.min_weight:
                self.min_weight = candidate_weight
                self.best_solution = candidate

        else:
            if random.random() < self.acceptance_probability(candidate_weight):
                self.curr_weight = candidate_weight
                self.curr_solution = candidate

    def anneal(self):
        '''
        Annealing process with 2-opt
        described here: https://en.wikipedia.org/wiki/2-opt
        '''
        while self.temp >= self.stopping_temp and self.iteration < self.stopping_iter:
            candidate = list(self.curr_solution)
            l = random.randint(2, self.sample_size - 1)
            i = random.randint(0, self.sample_size - l)

            candidate[i: (i + l)] = reversed(candidate[i: (i + l)])

            self.accept(candidate)
            self.temp *= self.alpha
            self.iteration += 1
            self.weight_list.append(self.curr_weight)
            self.solutionHistory.append(self.curr_solution)

        print('Minimum weight: ', self.min_weight)
        print('Improvement: ',
              round((self.initial_weight - self.min_weight) / (self.initial_weight), 4) * 100, '%')

        return [self.coords, self.solutionHistory]
