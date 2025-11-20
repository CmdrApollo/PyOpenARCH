# all the imports
import pygame
import math
from scripts.interface import *
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

    # camera variables
    camera: Vec2 = Vec2(10, -32)
    camera_drag: bool = False

    # world size
    world_width: int = 80
    world_height: int = 80

    # the actual tiles
    # TODO move to a class along with world size
    # generate ocean tiles by converting a one-dimensional
    # i-value to an (x,y) coordinate
    tiles: list[Tile] = [OceanTile(i % world_width, i // world_width, None) for i in range(world_width * world_height)]

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
            d: float = 1 - (math.sqrt(pow(x - world_width / 2, 2) + pow(y - world_height / 2 , 2)) / math.hypot(world_width / 2, world_height / 2))
            # scaled noise value based on distance
            n: float = ((1 + base_noise.noise((x / world_width, y / world_height))) / 2) * pow(d, 1.0 / 3.0)

            # TODO no magic numbers
            if n < 0.4:
                t = DeepOceanTile
            elif n < 0.5:
                t = OceanTile
            elif n < 0.52:
                t = BeachTile
            elif n < 0.625:
                if forest_noise((x / world_width, y / world_height)) < 0:
                    t = PlainsTile
                else:
                    t = ForestTile
            else:
                t = MountainTile

            # setting the tile
            tiles[y * world_width + x] = t(x, y, None)

    # helper for doing silly math
    def get_tile(x: int, y: int) -> Tile:
        return tiles[y * world_width + x]

    # window that needs to be referenced multipe times
    welcome_window = UIWindow(all_text["TITLE_WELCOME"], all_text["BODY_WELCOME"], pygame.Rect(width // 2 - 320, height // 2 - 240, 640, 480))

    # UI manager
    window_manager = WindowManager((width, height), [
        welcome_window,
        UIWindow(all_text["TITLE_TUTORIAL"], all_text["BODY_TUTORIAL"], pygame.Rect(width // 2 - 200, height // 2 - 150, 400, 300)),
    ])

    # function for the journal button
    def show_welcome():
        if welcome_window not in window_manager.windows:
            window_manager.add_window(welcome_window)

    # button manager
    button_manager = ButtonManager([
        UIButton(40, 40, 32, get_sprite("icon_menu")),
        UIButton(120, 40, 32, get_sprite("icon_journal"), show_welcome)
    ])

    # main loop
    running = True
    while running:
        # calculate delta-time with clock object
        delta = clock.tick_busy_loop(60.0) / 1000.0

        # avoid divide by 0 errors
        if delta != 0:
            window.title = f"{gamename} | {(1.0 / delta):.1f}fps"

        # get mouse position at the start of the frame
        mx, my = pygame.mouse.get_pos()

        # calculate world position of the mouse
        sx, sy = to_world(mx, my, camera)
        _c = get_sprite('_template').get_at(((mx - camera.x * tile_size.x) % tile_size.x, (my - camera.y * tile_size.y) % tile_size.y))
        
        # TODO cringe
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
            
            if camera_drag:
                # if panning the camera or dragging a window
                # manager eat the event
                event_valid: bool = True
            else:
                if window_manager.dragging:
                    # if a window is being dragged, skip
                    # the button manager
                    event_valid = True
                else:
                    # otherwise, check buttons first
                    # button manager tells whether or not it ate the event
                    event_valid: bool = button_manager.handle_event(event, mx, my)
                
                if event_valid:
                    # if the button manager didn't eat the thing or we
                    # are dragging a window, hand it off to the window manager
                    # then, window manager tells whether or not it ate the event
                    event_valid = window_manager.handle_event(event, mx, my)

            if event_valid:
                # we want to process the event here
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 2:
                        # middle mouse clicked on world tile
                        camera_drag = True
                    elif event.button == 3 and not camera_drag and not window_manager.dragging:
                        # RMB used on world tile
                        # show WIP status menu
                        tile: Tile = get_tile(sx, sy)
                        window_manager.add_status_menu(tile, mx, my)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 2:
                        # let go of middle mouse so stop dragging
                        camera_drag = False
                elif event.type == pygame.MOUSEMOTION:
                    if camera_drag:
                        # middle mouse drag, pan camera
                        camera.x += event.rel[0] / tile_size.x
                        camera.y += event.rel[1] / tile_size.y

        # drawing routine
        # fill the screen with black
        screen.fill('black')
       
        # draw each tile with its corresponding sprite
        for x in range(world_width):
            for y in range(world_height):
                screen_x, screen_y = to_screen(x, y, camera)
                screen.blit(get_sprite(get_tile(x, y).graphic), (screen_x, screen_y))

        # draw the selection marker
        screen.blit(get_sprite('select'), to_screen(sx, sy, camera))

        # draw the windows to the screen
        window_manager.draw(screen)

        # draw the buttons to the screen
        button_manager.draw(screen)

        # refresh the window
        window.flip()

    # after 'X' is hit, exit cleanly
    pygame.quit()

if __name__ == "__main__":
    # if this is the main file,
    # run the 'main' function
    main()