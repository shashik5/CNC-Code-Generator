from data_generator import DataGenerator
from code_generators.drilling import DrillingCNC, DrillConfig
from algorithms.simulated_annealing import SimulatedAnnealing
import visualizer
import json
import threading


def main():
    with open('data/data.json', 'r') as jsonfile:
        appConfig = json.load(jsonfile)
    
    # TODO: Move the below configurations into config.json file
    '''set the simulated annealing algorithm params'''
    temp = 1000
    stopping_temp = 0.00000001
    alpha = 0.9995
    stopping_iter = 10000000

    '''set the dimensions of the grid'''
    size_width = 200
    size_height = 200

    '''set the number of nodes'''
    population_size = 70

    nodes = DataGenerator(size_width, size_height, population_size).generate()

    sa = SimulatedAnnealing(nodes, temp, alpha, stopping_temp, stopping_iter)
    [coords, solution_history] = sa.anneal()

    t1 = threading.Thread(target=visualizer.animateTSP, args=(solution_history, coords))
    t1.start()

    cg = DrillingCNC(coords, solution_history[-1], DrillConfig(**appConfig['drillConfig']))
    # TODO: Create an UI to display the CNC code and provide the option to print
    print(cg.generateCode())


if __name__ == "__main__":
    main()
