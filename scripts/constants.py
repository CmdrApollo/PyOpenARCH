import pygame

# initialize everything
pygame.init()

# Vector2 alias
Vec2 = pygame.Vector2

# the path to the font used by the game
fontname = "assets/fonts/RobotoMono-Regular.ttf"

# font constants
SMALL_FONT = pygame.font.Font(fontname, 16)
FONT = pygame.font.Font(fontname, 20)
BIG_FONT = pygame.font.Font(fontname, 24)

# the name of the game
gamename = "PyOpenARCH"

# window/drawing setup
width, height = 1600, 900
window = pygame.Window(title=gamename, size=(width, height))
screen = window.get_surface()

# tile constants
tile_size = pygame.Vector2(64, 32)

# external sprites
lines = pygame.image.load("assets/sprites/scanlines_full.png").convert_alpha().subsurface((0, 0, width, height))
SPRITES = {}
for f in ["assets\\sprites\\_template.png"]:
    n = f.split('\\')[-1].split('.')[0]
    SPRITES.update({ n: pygame.transform.scale(pygame.image.load(f).convert_alpha(), tile_size) })

# generated sprites
for pair in [
    ('base', '#c0c0c0'), # unused
    ('grass', '#00ff00'),
    ('forest', '#008000'),
    ('dirt', '#ff8000'),
    ('sand', '#ffff00'),
    ('water', '#0000ff'),
    ('deep_water', '#000080'),
    ('select', '#00ffff')
]:
    # make the surface
    s = pygame.Surface(tile_size, pygame.SRCALPHA)
    # draw the iso tile
    pygame.draw.polygon(s, pair[1], [
        (tile_size[0] // 2, 0),
        (tile_size[0], tile_size[1] // 2),
        (tile_size[0] // 2, tile_size[1]),
        (0, tile_size[1] // 2)
    ])
    # select has half alpha
    if pair[0] == "select":
        s.set_alpha(128)
    # add to the dictionary
    SPRITES.update({pair[0]: s})

# helper functions
def clamp(a: float, b: float, c: float) -> float:
    return min(max(a, b), c)

def get_sprite(s: str) -> pygame.Surface:
    spr: pygame.Surface = SPRITES[s]
    return spr