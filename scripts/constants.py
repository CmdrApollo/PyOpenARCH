import pygame

# initialize everything
pygame.init()

# Vector2 alias
Vec2 = pygame.Vector2

# the path to the font used by the game
fontname = "assets/fonts/RobotoMono-Regular.ttf"

# font constants
small_font = pygame.font.Font(fontname, 16)
font = pygame.font.Font(fontname, 20)
big_font = pygame.font.Font(fontname, 24)

# the name of the game
gamename = "PyOpenARCH"

# window/drawing setup
width, height = 1600, 900
button = pygame.Window(title=gamename, size=(width, height))
screen = button.get_surface()

# tile constants
tile_size = pygame.Vector2(64, 32)

# external sprites
SPRITES = {}

# non-scaled external sprites
# TODO gross
for f in [
    f"assets\\sprites\\icon_{i}.png"
    for i in ["menu", "journal"]
]:
    n = f.split('\\')[-1].split('.')[0]
    SPRITES.update({ n: pygame.image.load(f).convert_alpha() })

# scaled external sprite(s)
# TODO gross
for f in ["assets\\sprites\\_template.png"]:
    n = f.split('\\')[-1].split('.')[0]
    SPRITES.update({ n: pygame.transform.scale(pygame.image.load(f).convert_alpha(), tile_size) })

terrain = pygame.image.load("assets\\sprites\\terrain.png").convert_alpha()
terrain_sprites_per_line = 4

# terrain sprites
for i, name in enumerate([
        'base',
        'grass',
        'forest',
        'mountain',
        'sand',
        'water',
        'deep_water',
        'select',
    ]):
    x = i % terrain_sprites_per_line
    y = i // terrain_sprites_per_line
    SPRITES.update({name: terrain.subsurface((x * tile_size.x, y * tile_size.y, tile_size.x, tile_size.y))})

# helper functions
def clamp(a: float, b: float, c: float) -> float:
    return min(max(a, b), c)

def get_sprite(s: str) -> pygame.Surface:
    spr: pygame.Surface = SPRITES[s]
    return spr