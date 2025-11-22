# all the imports
import pygame

from scripts.world import World
from scripts.constants import window, screen

# the main function that get's called
# upon game startup
def main() -> None:
    # make the clock and initialize the delta-time
    clock = pygame.time.Clock()
    delta: float = 0.0

    # the most important thing that handles all the
    # rendering and management of all the systems
    world: World = World()

    # main loop
    running = True
    while running:
        # calculate delta-time with clock object
        delta = clock.tick_busy_loop(60.0) / 1000.0

        # main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # if the 'X' is pressed, close the window
                running = False
            else:
                # if it is not an exit event, pass it off
                # to the world and let it handle the event
                world.handle_event(event)

        # master list of keys
        keys = pygame.key.get_pressed()

        # show_factions is only true if tab is pressed
        show_factions = keys[pygame.K_TAB]

        # drawing routine
        # fill the screen with black
        screen.fill('black')

        # tell the world to draw itself
        world.draw(screen, show_factions)

        # refresh the window
        window.flip()

    # after 'X' is hit, exit cleanly
    pygame.quit()

if __name__ == "__main__":
    # if this is the main file,
    # run the 'main' function
    main()