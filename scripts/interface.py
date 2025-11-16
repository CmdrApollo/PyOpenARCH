import pygame
from .constants import *

# main UI window class
class UIWindow:
    def __init__(self, title: str, body: str, rect: pygame.Rect, can_close: bool = True, z: float = 1):
        self.title = title
        self.body = body
        self.rect = rect
        self.can_close = can_close
        self.z_value = z

        self.topbar_height = 40
        self.dragging = False

        self.to_remove = False

    def draw(self, screen: pygame.Surface) -> None:
        # make text surfaces
        title = SMALL_FONT.render(self.title, True, "white", wraplength=self.rect.width-20)
        body = FONT.render(self.body, True, "white", wraplength=self.rect.width-20)
        # draw rectangles
        pygame.draw.rect(screen, 'black', self.rect)
        pygame.draw.rect(screen, 'white', self.rect, 1)
        # draw seperator line
        self.topbar_height = title.height + 20
        pygame.draw.line(screen, 'white', (self.rect.left, self.rect.y + title.height + 20), (self.rect.right - 1, self.rect.y + self.topbar_height))
        # blit text surfaces
        screen.blit(title, (self.rect.x + 10, self.rect.y + 10))
        screen.blit(body, (self.rect.x + 10, self.rect.y + title.height + 30))
        # blit red 'X'
        screen.blit(s := SMALL_FONT.render('X', True, 'red' if self.can_close else 'gray'), (self.rect.right - s.width - 10, self.rect.y + 10))

    def handle_event(self, manager, event: pygame.Event, mx: int, my: int):
        # 'internal x' and 'internal y' (i.e. how far into the window the mouse is)
        ix, iy = mx - self.rect.x, my - self.rect.y

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # LMB
                if ix > self.rect.width - self.topbar_height and iy < self.topbar_height:
                    # top right corner (the 'X')
                    if self.can_close:
                        self.to_remove = True
                elif ix < self.rect.bottom - self.topbar_height and iy < self.topbar_height:
                    # in top bar but not top right corner
                    self.dragging = True
                    manager.put_on_top(self)
                else:
                    manager.put_on_top(self)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                # let go of LMB = not dragging
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                # LMB dragged
                # move window based on relative mouse movement and clamp to the screen size
                self.rect.x = clamp(self.rect.x + event.rel[0], 0, width - self.rect.width)
                self.rect.y = clamp(self.rect.y + event.rel[1], 0, height - self.rect.height)

# main UI window class
class UIStatusMenu(UIWindow):
    def __init__(self, title, body, rect, z = 1):
        super().__init__(title, body, rect, False, z)

    def draw(self, screen: pygame.Surface) -> None:
        # make text surfaces
        title = SMALL_FONT.render(self.title, True, "white", wraplength=self.rect.width-20)
        body = FONT.render(self.body, True, "white", wraplength=self.rect.width-20)
        # draw rectangles
        pygame.draw.rect(screen, 'black', self.rect)
        pygame.draw.rect(screen, 'white', self.rect, 1)
        # draw seperator line
        self.topbar_height = title.height + 20
        pygame.draw.line(screen, 'white', (self.rect.left, self.rect.y + title.height + 20), (self.rect.right - 1, self.rect.y + self.topbar_height))
        # blit text surfaces
        screen.blit(title, (self.rect.x + 10, self.rect.y + 10))
        screen.blit(body, (self.rect.x + 10, self.rect.y + title.height + 30))

# main window management class
class WindowManager:
    def __init__(self, size: tuple[int, int], windows: list[UIWindow]):
        self.width, self.height = size
        self.windows = windows
    
    def draw(self, screen: pygame.Surface) -> None:
        # call draw method on all windows which are sorted by
        # z_value in the handle_event method on this class
        for w in self.windows:
            w.draw(screen)
    
    def add_window(self, window: UIWindow):
        self.windows.append(window)
        self.put_on_top(window)

    def put_on_top(self, window: UIWindow):
        # make the selected window have an infinite z value
        window.z_value = float('inf')

        # sort the windows again
        self.windows.sort(key=lambda x: x.z_value)
        
        # "normalize" z values
        for i, w in enumerate(self.windows):
            w.z_value = i + 1

    def handle_event(self, event: pygame.Event, mx: int, my: int) -> bool:
        # sort windows by z value
        self.windows.sort(key=lambda x: x.z_value)

        # top most window under mouse gets selected
        window = None
        for w in self.windows:
            if w.rect.collidepoint(mx, my):
                window = w
            elif isinstance(w, UIStatusMenu):
                w.to_remove = True
        
        # get rid of dead windows
        for w in self.windows[::-1]:
            if w.to_remove:
                self.windows.remove(w)
        
        # if a window is hovered over,
        # let it handle the event
        if window is not None:
            window.handle_event(self, event, mx, my)

            # remove a window if it requests
            # to be gone
            if window.to_remove:
                self.windows.remove(window)
            
            # return false because a window ate the click
            return False
    
        # no window ate the click
        return True

class UIButton:
    def __init__(self, x: int, y: int, r: int, icon: pygame.Surface = None):
        self.position = Vec2(x, y)
        self.radius = r
        self.icon = icon
    
    def draw(self, screen):
        pygame.draw.circle(screen, 'black', self.position, self.radius)
        pygame.draw.circle(screen, 'white', self.position, self.radius, 1)
        screen.blit(self.icon, (self.position.x - self.icon.width / 2, self.position.y - self.icon.height / 2))