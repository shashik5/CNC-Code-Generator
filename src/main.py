from app_config import AppConfig
from data_config import DataConfig
from data_generator import DataGenerator
from code_generators.drilling import DrillingCNC
from algorithms.simulated_annealing import SimulatedAnnealing
import tkinter as tk
from utils import copyToClipboard
import visualizer
import json


def main():
    with open('data/data.json', 'r') as jsonfile:
        data = DataConfig(**json.load(jsonfile))

    with open('src/config.json', 'r') as jsonfile:
        appConfig = AppConfig(**json.load(jsonfile))

    saConfig = appConfig.simulatedAnnealing
    workpieceSize = appConfig.workpieceSize

    nodes = DataGenerator(workpieceSize.width, workpieceSize.height,
                          appConfig.numberOfDrillPoints).generate()

    sa = SimulatedAnnealing(nodes, saConfig)
    [coords, solutionHistory] = sa.anneal()

    def generateCode():
        cg = DrillingCNC(coords, solutionHistory[-1], data.drillConfig)
        code = cg.generateCode()
        window = tk.Tk()
        window.title('CNC Code')
        frame = tk.Frame(master=window)
        frame.pack()

        frame1 = tk.Frame(master=window, width=750, height=30)
        frame1.pack()
        text = tk.Text(master=frame)
        text.insert(tk.INSERT, code)
        text.configure(width=100, height=30, state='disabled')
        button = tk.Button(master=frame1, text='Copy code to clipboard')

        def onClick(arg):
            copyToClipboard(code)
            msg = tk.Message(master=frame1, text="Code Copied!", width=200)
            msg.place(x=150, y=5)

        button.bind('<Button-1>', onClick)
        text.pack()
        button.place(x=0, y=0)
        window.mainloop()

    visualizer.animateTSP(solutionHistory, coords, generateCode)


if __name__ == "__main__":
    main()
