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

# important game variables
gamename = "PyOpenARCH"
gameversion = "v0.0.1"
gamenameandversion = f"{gamename} {gameversion}"

# window/drawing setup
width, height = 1600, 900
window = pygame.Window(title=gamenameandversion, size=(width, height))
screen = window.get_surface()

# tile constants
tile_size = pygame.Vector2(64, 32)

# external sprites
SPRITES = {}

# non-scaled external sprites
for f in ["icon_menu", "icon_journal"]:
    SPRITES.update({ f: pygame.image.load(f"assets\\sprites\\{f}.png").convert_alpha() })

# scaled external sprite(s)
for f in ["_template"]:
    SPRITES.update({ f: pygame.transform.scale(pygame.image.load(f"assets\\sprites\\{f}.png").convert_alpha(), tile_size) })

terrain = pygame.image.load("assets\\sprites\\terrain.png").convert_alpha()
terrain_sprites_per_line = 4

# terrain sprites
for i, name in enumerate([
        'base',
        'grass',
        'forest',
        'farmland',
        'mountain',
        'sand',
        'water',
        'deep_water',
    ]):
    x = i % terrain_sprites_per_line
    y = i // terrain_sprites_per_line
    SPRITES.update({name: terrain.subsurface((x * tile_size.x, y * tile_size.y, tile_size.x, tile_size.y))})

select = SPRITES['base'].copy()
select.fill('cyan', special_flags=pygame.BLEND_RGB_MULT)
select.set_alpha(128)
SPRITES.update({'select': select})

# helper functions
def clamp(a: float, b: float, c: float) -> float:
    return min(max(a, b), c)

def get_sprite(s: str) -> pygame.Surface:
    spr: pygame.Surface = SPRITES[s]
    return spr