# all the imports
import pygame
import math
from scripts.window import *
from scripts.constants import *
from scripts.tile import *
from scripts.text import *

import perlin_noise

# coordinate functions
# TODO maybe use Vector outputs as well?
def to_screen(x: float, y: float, cam: Vec2) -> tuple[float, float]:
    return (
        cam.x * tile_size.x + (x - y) * (tile_size.x // 2),
        cam.y * tile_size.y + (x + y) * (tile_size.y // 2)
    )

def to_world(x: float, y: float, cam: Vec2) -> tuple[float, float]:
    return (
        ((y - cam.y * tile_size.y) // tile_size.y) + ((x - cam.x * tile_size.x) // tile_size.x),
        ((y - cam.y * tile_size.y) // tile_size.y) - ((x - cam.x * tile_size.x) // tile_size.x)
    )

# the main function that get's called
# upon game startup
def main() -> None:
    # get some global variables
    global tile_size, SPRITES

    # make the clock and initialize the delta-time
    clock = pygame.time.Clock()
    delta: float = 0.0

    # camera position
    camera = Vec2(10, -32)

    # world size
    world_width = 100
    world_height = 100

    # the actual tiles
    # TODO move to a class along with world size
    tiles = [[WaterTile(i, j) for i in range(world_width)] for j in range(world_height)]

    # perlin noise objects
    # TODO no magic numbers
    base_noise = perlin_noise.PerlinNoise(9.17)
    forest_noise = perlin_noise.PerlinNoise(6.41)

    # world generation
    # TODO move into a class along with the
    #      other world things
    for x in range(world_width):
        for y in range(world_height):
            # distance from center of the world
            d = 1 - (math.sqrt(pow(x - world_width / 2, 2) + pow(y - world_height / 2 , 2)) / math.hypot(world_width / 2, world_height / 2))
            # scaled noise value based on distance
            n = ((1 + base_noise.noise((x / world_width, y / world_height))) / 2) * pow(d, 1.0 / 3.0)

            # TODO no magic numbers
            if n < 0.4:
                t = DeepWaterTile
            elif n < 0.5:
                t = WaterTile
            elif n < 0.52:
                t = SandTile
            else:
                if forest_noise((x / world_width, y / world_height)) < 0:
                    t = GrassTile
                else:
                    t = ForestTile

            # setting the tile
            tiles[y][x] = t(x, y)

    # UI manager
    manager = UIManager((width, height), [
        UIWindow(all_text["TITLE_TUTORIAL"], all_text["BODY_TUTORIAL"], pygame.Rect(width // 2 - 200, height // 2 - 150, 400, 300)),
        UIWindow(all_text["TITLE_WELCOME"], all_text["BODY_WELCOME"], pygame.Rect(width // 2 - 320, height // 2 - 240, 640, 480)),
        UIWindow("Test", "Another window for testing.", pygame.Rect(width // 2 - 320, height // 2 - 240, 400, 300)),
    ])

    # main loop
    running = True
    while running:
        # calculate delta-time with clock object
        delta = clock.tick_busy_loop(60) / 1000

        # get mouse position at the start of the frame
        mx, my = pygame.mouse.get_pos()

        # calculate world position of the mouse
        sx, sy = to_world(mx, my, camera)
        _c = get_sprite('_template').get_at(((mx - camera.x * tile_size.x) % tile_size.x, (my - camera.y * tile_size.y) % tile_size.y))
        
        # cringe
        match _c.r, _c.g, _c.b:
            case 255, 0, 0:
                sx -= 1
            case 0, 255, 0:
                sy -= 1
            case 0, 0, 255:
                sx += 1
            case 255, 255, 0:
                sy += 1

        # finish calculating mouse world position
        sx = clamp(int(sx), 0, world_width - 1)
        sy = clamp(int(sy), 0, world_height - 1)

        # main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # if the 'X' is pressed, close the window
                running = False
            
            # manager tells whether or not it ate the event
            event_valid: bool = manager.handle_event(event, mx, my)

            if event_valid:
                # we want to process the event here
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # RMB used on world tile
                    if event.button == 3:
                        # show WIP status menu
                        w = UIStatusMenu("Status", "Cabrón", pygame.Rect(mx - 80, my - 100, 160, 200))
                        manager.windows.append(w)
                        manager.put_on_top(w)

        # master list of keys
        keys = pygame.key.get_pressed()

        # move the camera based on WASD
        camera.x -= delta * (keys[pygame.K_d] - keys[pygame.K_a]) * 8
        camera.y -= delta * (keys[pygame.K_s] - keys[pygame.K_w]) * 8

        # drawing routine
        # fill the screen the same color as the dark water
        screen.fill('#000080')
       
        # draw each tile with its corresponding sprite
        for x in range(world_width):
            for y in range(world_height):
                screen_x, screen_y = to_screen(x, y, camera)
                screen.blit(get_sprite(tiles[y][x].graphic), (screen_x, screen_y))

        # draw the selection marker
        screen.blit(get_sprite('select'), to_screen(sx, sy, camera))
        
        # TODO this probably can go
        for x in range(world_width):
            for y in range(world_height):
                for e in tiles[y][x].entities:
                    screen_x, screen_y = to_screen(x - 1, y - 1, camera)
                    if e.graphic == 'water':
                        screen_y + math.sin((x + y) * pygame.time.get_ticks() // 2)
                    screen.blit(get_sprite(e.graphic), (screen_x, screen_y))

        manager.draw(screen)

        # scanlines
        screen.blit(lines)

        # refresh the window
        window.flip()

    # after 'X' is hit, exit cleanly
    pygame.quit()

if __name__ == "__main__":
    # if this is the main file,
    # run the 'main' function
    main()