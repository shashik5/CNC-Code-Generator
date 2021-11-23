from algorithms.simulated_annealing import SimulatedAnnealingConfig


class AppConfig:
    def __init__(self, simulatedAnnealing: SimulatedAnnealingConfig) -> None:
        self.simulatedAnnealing = SimulatedAnnealingConfig(
            **simulatedAnnealing)
