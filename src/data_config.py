from code_generators.drilling import DrillConfig


class DataConfig:
    def __init__(self, drillConfig: DrillConfig) -> None:
        self.drillConfig = DrillConfig(**drillConfig)
