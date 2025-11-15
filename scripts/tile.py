class Tile:
    def __init__(self, x, y, gfx):
        self.entities = []
        self.x, self.y = x, y
        self.graphic = gfx

class BaseTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y, 'base')

class GrassTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y, 'grass')

class ForestTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y, 'forest')

class DirtTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y, 'dirt')

class SandTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y, 'sand')

class WaterTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y, 'water')

class DeepWaterTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y, 'deep_water')