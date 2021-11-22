from algorithms.simulated_annealing import SimulatedAnnealingConfig


class WorkpieceSize:
    def __init__(self, height, width) -> None:
        self.height = height
        self.width = width


class AppConfig:
    def __init__(self, simulatedAnnealing: SimulatedAnnealingConfig, workpieceSize: WorkpieceSize, numberOfDrillPoints: int) -> None:
        self.numberOfDrillPoints = numberOfDrillPoints
        self.simulatedAnnealing = SimulatedAnnealingConfig(
            **simulatedAnnealing)
        self.workpieceSize = WorkpieceSize(**workpieceSize)
