from .colony import *

class Tile:
    def __init__(self, x, y, colony: Colony | None, gfx):
        self.x, self.y = x, y
        self.colony = colony
        self.graphic = gfx

class BaseTile(Tile):
    def __init__(self, x, y, colony):
        super().__init__(x, y, colony, 'base')

class GrassTile(Tile):
    def __init__(self, x, y, colony):
        super().__init__(x, y, colony, 'grass')

class ForestTile(Tile):
    def __init__(self, x, y, colony):
        super().__init__(x, y, colony, 'forest')

class DirtTile(Tile):
    def __init__(self, x, y, colony):
        super().__init__(x, y, colony, 'dirt')

class SandTile(Tile):
    def __init__(self, x, y, colony):
        super().__init__(x, y, colony, 'sand')

class WaterTile(Tile):
    def __init__(self, x, y, colony):
        super().__init__(x, y, colony, 'water')

class DeepWaterTile(Tile):
    def __init__(self, x, y, colony):
        super().__init__(x, y, colony, 'deep_water')