import pygame
from .constants import get_sprite

class Faction:
    def __init__(self, name: str, color: str = 'white', home_x: int = 0, home_y: int = 0):
        self.name = name
        self.color = color
        self.home_x = home_x
        self.home_y = home_y

        self.make_tile()
    
    def make_tile(self):
        self.surface = get_sprite('base').copy()

        self.surface.fill(self.color, special_flags=pygame.BLEND_RGB_MULT)
        self.surface.set_alpha(128)