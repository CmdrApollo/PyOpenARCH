import math
import random
import perlin_noise

from scripts.interface import UIButton, UIWindow, ButtonManager, WindowManager
from scripts.tile import Tile, OceanTile, DeepOceanTile, BeachTile, PlainsTile, ForestTile, MountainTile
from scripts.text import all_text
from scripts.factions import Faction
from scripts.constants import *

class World:
    def __init__(self):
        # camera variables
        self.camera: Vec2 = Vec2(0, 0)
        self.camera_drag: bool = False

        # world size
        self.world_width: int = 128
        self.world_height: int = 128

        # selected tile
        self.selected_x: int = 0
        self.selected_y: int = 0

        # faction variables
        self.num_factions: int = 9

        faction_colors: list[str] = [
            'red',
            'orange',
            'yellow',
            'green',
            'forestgreen',
            'blue',
            'indigo',
            'purple',
            'pink',
            'white',
        ]

        self.factions: list[Faction] = [
            Faction(
                chr(65 + i),
                faction_colors[i],
                random.randint(0, self.world_width - 1),
                random.randint(0, self.world_height - 1)
            )
            for i in range(self.num_factions)
        ]

        self.show_factions: bool = False

        # the actual tiles
        self.tiles: list[Tile] = [None for _ in range(self.world_width * self.world_height)]

        # perlin noise objects
        # TODO no magic numbers
        base_noise = perlin_noise.PerlinNoise(9.17)
        forest_noise = perlin_noise.PerlinNoise(6.41)

        # world generation
        for x in range(self.world_width):
            for y in range(self.world_height):
                # distance from center of the world
                d: float = 1 - (math.sqrt(pow(x - self.world_width / 2, 2) + pow(y - self.world_height / 2 , 2)) / math.hypot(self.world_width / 2, self.world_height / 2))
                # scaled noise value based on distance
                n: float = ((1 + base_noise.noise((x / self.world_width, y / self.world_height))) / 2) * pow(d, 1.0 / 3.0)

                # TODO no magic numbers
                if n < 0.4:
                    t = DeepOceanTile
                elif n < 0.5:
                    t = OceanTile
                elif n < 0.52:
                    t = BeachTile
                elif n < 0.625:
                    # set either plains or forest based on the secondary noise source
                    if forest_noise.noise((x / self.world_width, y / self.world_height)) < 0:
                        t = PlainsTile
                    else:
                        t = ForestTile
                else:
                    t = MountainTile

                # figure out the closest faction hq so it can be assigned
                closest_faction: Faction = None
                closest_distance: float = float('inf')

                for f in self.factions:
                    d = math.sqrt(pow(f.home_x - x, 2) + pow(f.home_y - y, 2))
                    
                    if d < closest_distance:
                        closest_distance = d
                        closest_faction = f

                # setting the tile
                self.tiles[y * self.world_width + x] = t(x, y, closest_faction, None)

        # window that needs to be referenced multipe times
        self.welcome_window = UIWindow(all_text["TITLE_WELCOME"], all_text["BODY_WELCOME"], pygame.Rect(width // 2 - 320, height // 2 - 240, 640, 480))

        # UI manager
        self.window_manager = WindowManager((width, height), [
            self.welcome_window,
            UIWindow(all_text["TITLE_TUTORIAL"], all_text["BODY_TUTORIAL"], pygame.Rect(width // 2 - 200, height // 2 - 150, 400, 300)),
        ])

        # function for the journal button
        # TODO temp
        def show_welcome():
            if self.welcome_window not in self.window_manager.windows:
                self.window_manager.add_window(self.welcome_window)

        # button manager
        self.button_manager = ButtonManager([
            UIButton(40, 40, 32, get_sprite("icon_menu")),
            UIButton(120, 40, 32, get_sprite("icon_journal"), show_welcome)
        ])

        max_screen_x = max_screen_y = 0
        min_screen_x = min_screen_y = 1_000_000 # arbitrary big number

        # TODO this is a weird hack with the +2/+1, but it fixes an issue
        for x in range(self.world_width + 2):
            for y in range(self.world_height + 1):
                sx, sy = to_screen(x, y, Vec2(0, 0))

                max_screen_x = max(max_screen_x, sx)
                min_screen_x = min(min_screen_x, sx)

                max_screen_y = max(max_screen_y, sy)
                min_screen_y = min(min_screen_y, sy)

        # calculate stuff for the surfaces to be generated
        # namely size and start position
        surf_width, surf_height = max_screen_x - min_screen_x, max_screen_y - min_screen_y
        start_cam = Vec2(-min_screen_x // tile_size.x, -min_screen_y // tile_size.y)

        # the surfaces themselves
        self.world_surface = pygame.Surface((surf_width, surf_height))
        self.factions_surface = pygame.Surface((surf_width, surf_height), pygame.SRCALPHA)

        # draw onto the world surfaces
        for x in range(self.world_width):
            for y in range(self.world_height):
                self.world_surface.blit(get_sprite(self.get_tile(x, y).graphic), to_screen(x, y, start_cam))
                self.factions_surface.blit(self.get_tile(x, y).faction.surface, to_screen(x, y, start_cam))

        # important for drawing the world
        self.draw_start_tile = to_world(0, 0, start_cam)

    # helper for doing silly math
    def get_tile(self, x: int, y: int) -> Tile:
        return self.tiles[y * self.world_width + x]

    def screen_to_tile_xy(self, x: int, y: int) -> tuple[int, int]:
        # calculate world position of the mouse
        sx, sy = to_world(x, y, self.camera)
        _c = get_sprite('_template').get_at(((x - self.camera.x * tile_size.x) % tile_size.x, (y - self.camera.y * tile_size.y) % tile_size.y))
        
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
        sx = clamp(int(sx), 0, self.world_width - 1)
        sy = clamp(int(sy), 0, self.world_height - 1)

        return (sx, sy)

    def handle_event(self, event: pygame.Event) -> None:
        mx, my = pygame.mouse.get_pos()
        self.selected_x, self.selected_y = self.screen_to_tile_xy(mx, my)

        if self.camera_drag:
            # if panning the camera or dragging a window
            # manager eat the event
            event_valid: bool = True
        else:
            if self.window_manager.dragging:
                # if a window is being dragged, skip
                # the button manager
                event_valid = True
            else:
                # otherwise, check buttons first
                # button manager tells whether or not it ate the event
                event_valid: bool = self.button_manager.handle_event(event, mx, my)
            
            if event_valid:
                # if the button manager didn't eat the thing or we
                # are dragging a window, hand it off to the window manager
                # then, window manager tells whether or not it ate the event
                event_valid = self.window_manager.handle_event(event, mx, my)

        if event_valid:
            # we want to process the event here
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    # middle mouse clicked on world tile
                    self.camera_drag = True
                elif event.button == 3 and not self.camera_drag and not self.window_manager.dragging:
                    # RMB used on world tile
                    # show WIP status menu
                    tile: Tile = self.get_tile(self.selected_x, self.selected_y)
                    self.window_manager.add_status_menu(tile, mx, my)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:
                    # let go of middle mouse so stop dragging
                    self.camera_drag = False
            elif event.type == pygame.MOUSEMOTION:
                if self.camera_drag:
                    # middle mouse drag, pan camera
                    self.camera.x += event.rel[0] / tile_size.x
                    self.camera.y += event.rel[1] / tile_size.y
    
    def draw(self, screen: pygame.Surface, show_factions: bool = False) -> None:
        # draw the world
        screen.blit(self.world_surface, to_screen(*self.draw_start_tile, self.camera))
        # if instructed, draw the factions
        if show_factions:
            screen.blit(self.factions_surface, to_screen(*self.draw_start_tile, self.camera))

        # draw the selection marker
        screen.blit(get_sprite('select'), to_screen(self.selected_x, self.selected_y, self.camera))

        # draw the windows to the screen
        self.window_manager.draw(screen)

        # draw the buttons to the screen
        self.button_manager.draw(screen)