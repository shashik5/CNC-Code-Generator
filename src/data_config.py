from code_generators.drilling import DrillingConfig


class WorkpieceSize:
    def __init__(self, height, width) -> None:
        self.height = height
        self.width = width


class DataConfig:
    def __init__(self, drillingConfig: DrillingConfig, workpieceSize: WorkpieceSize) -> None:
        self.drillingConfig = DrillingConfig(**drillingConfig)
        self.workpieceSize = WorkpieceSize(**workpieceSize)
