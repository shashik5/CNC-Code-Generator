from numpy import array
from code_generators.position import Position


class DrillConfig:
    def __init__(self, isInInches: bool, isPathIncremental: bool, safePosition: Position, isFeedInMinutes: bool, workpieceThickness: float, feedRate: float, spindleSpeed: int):
        self.isInInches = isInInches
        self.isPathIncremental = isPathIncremental
        self.safePosition = Position(**safePosition)
        self.isFeedInMinutes = isFeedInMinutes
        self.workpieceThickness = workpieceThickness
        self.feedRate = feedRate
        self.spindleSpeed = spindleSpeed


class DrillingCNC:
    def __init__(self, coords: list, path: list, config: DrillConfig):
        self.coords = coords.copy()
        self.path = path.copy()
        self.lineCount = 0
        self.config = config

    def generateCode(self):
        self.lineCount = 0
        code = self._getStartCode() + self._moveToInitialPosition(
            self._getPositionById(self.path.pop(0)), False) + self._makeInitialDrill() + self._retractDrill()

        # TODO: Handle incremental path scenario
        for p in self.path:
            pos = self._getPositionById(p)
            code += self._moveToPosition(pos.x, pos.y) + \
                self._makeDrill() + self._retractDrill()

        code += self._moveToInitialPosition(
            self.config.safePosition, True) + self._endProgram()

        return code

    def _getSequenceNumber(self):
        lineNum = self.lineCount
        self.lineCount += 1
        return 'N{:03d}'.format(lineNum)

    def _getStartCode(self):
        cfg = self.config
        return '{} G{} G{} X{} Y{} Z{}\n'.format(self._getSequenceNumber(), 20 if cfg.isInInches else 21, 91 if cfg.isPathIncremental else 90, cfg.safePosition.x, cfg.safePosition.y, cfg.safePosition.z)

    def _moveToInitialPosition(self, position: Position, stopSpindle: bool):
        return '{} G00 X{} Y{}'.format(self._getSequenceNumber(), position.x, position.y) + (' M05' if stopSpindle else ' Z{}'.format(position.z)) + '\n'

    def _makeInitialDrill(self):
        cfg = self.config
        return '{} G01 G{} Z-{} F{} S{} M03\n'.format(self._getSequenceNumber(), 94 if cfg.isFeedInMinutes else 95, self._getDrillDepth(), cfg.feedRate, cfg.spindleSpeed)

    def _getDrillDepth(self):
        cfg = self.config
        return cfg.workpieceThickness + (0.4 if cfg.isInInches else 3)

    def _makeDrill(self):
        cfg = self.config
        return '{} G01 Z-{} F{}\n'.format(self._getSequenceNumber(), self._getDrillDepth(), cfg.feedRate)

    def _retractDrill(self):
        cfg = self.config
        return '{} G01 Z{}\n'.format(self._getSequenceNumber(), cfg.safePosition.z)

    def _moveToPosition(self, x, y):
        cfg = self.config
        return '{} G00 X{} Y{}\n'.format(self._getSequenceNumber(), x, y)

    def _endProgram(self):
        return '{} M30\n'.format(self._getSequenceNumber())

    def _getPositionById(self, id):
        cfg = self.config
        [x, y] = self.coords[id]
        return Position(x, y, cfg.safePosition.z)
