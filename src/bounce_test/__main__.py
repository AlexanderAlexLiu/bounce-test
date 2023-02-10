import pygame as pg
import numpy as np
import sys

class Color:
    WHITE = (251, 251, 242)
    RED = (255, 29, 21)
    GREEN = (62, 195, 0)
    BLACK = (35, 28, 7)
    GREY = (200, 200, 200)
    BLUE = (100, 100, 250)

class BounceTest:
    class Point:
        RADIUS = 10
        def __init__(self, x : int, y : int, color : tuple[int]) -> None:
            self.x, self.y = x, y
            self.mouse_x, self.mouse_y = 0, 0
            self.color = color
            self.clicked = False
        def is_collide(self, pos : tuple[int]) -> bool:
            x, y = pos
            return (self.x-x)**2 + (self.y-y)**2 < self.RADIUS**2
        def handle_event(self, event : pg.event.Event) -> None:
            match event.type:
                case pg.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.is_collide(event.pos):
                        self.clicked = True
                case pg.MOUSEBUTTONUP:
                    if event.button == 1 and self.clicked:
                        self.clicked = False
                case pg.MOUSEMOTION:
                    self.rel_x, self.rel_y = event.rel
        def update(self, box_rect : pg.Rect, box_thickness : int) -> None:
            if self.clicked:
                self.x += self.rel_x
                self.y += self.rel_y
                self.rel_x, self.rel_y = 0, 0
            if self.x < (box_rect.left + box_thickness):
                self.x = (box_rect.left + box_thickness)
            elif self.x > (box_rect.right - box_thickness):
                self.x = (box_rect.right - box_thickness)
            if self.y < (box_rect.top + box_thickness):
                self.y = (box_rect.top + box_thickness)
            elif self.y > (box_rect.bottom - box_thickness):
                self.y = (box_rect.bottom - box_thickness)
                '''
                self.delta_x = self.mouse_x - self.x
                self.delta_y = self.mouse_y - self.y
                self.delta_x = self.delta_x / 10
                self.delta_y = self.delta_y / 10
                self.x += self.delta_x
                self.y += self.delta_y
                self.x = self.x
                self.y = self.y
                '''
        def draw(self, surface : pg.Surface) -> None:
            pg.draw.circle(surface, self.color, (self.x, self.y), self.RADIUS)
        def get_pos(self) -> tuple:
            return (self.x, self.y)
    def decorate_window(self) -> None:
        pg.display.set_caption("Box-Point Vector Problem Simulation")
        pg.display.set_icon(pg.Surface((0,0)))
    def __init__(self) -> None:
        self.surface = pg.display.set_mode((800, 600), pg.NOFRAME | pg.HIDDEN)
        self.configure_events()
        self.decorate_window()
        self.clock = pg.time.Clock()
        self.point_A = self.Point(200, 300, Color.RED)
        self.point_B = self.Point(600, 300, Color.GREEN)
        self.box_rect = pg.Rect(100, 100, 600, 400)
        self.box_thickness = 1
    def configure_events(self) -> None:
        pg.event.set_blocked(None)
        pg.event.set_allowed((pg.MOUSEMOTION, pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP, pg.QUIT, pg.KEYUP, pg.KEYDOWN))
    def quit(self) -> None:
        pg.quit()
        sys.exit()
    def show_window(self) -> None:
        self.surface = pg.display.set_mode((800, 600), pg.NOFRAME | pg.SHOWN)
    def run(self) -> None:
        self.show_window() # avoid the blank screen at the start
        while 1:
            for event in pg.event.get():
                print(event)
                match event.type:
                    case pg.QUIT:
                        self.quit()
                    case pg.KEYDOWN:
                        match event.key:
                            case 27:
                                self.quit()
                            case 114:
                                self.point_A.x, self.point_A.y = 200, 300
                                self.point_B.x, self.point_B.y = 600, 300
                self.point_A.handle_event(event)
                self.point_B.handle_event(event)
            # UPDATES
            self.point_A.update(self.box_rect, self.box_thickness)
            self.point_B.update(self.box_rect, self.box_thickness)
            # ALWAYS HERE
            self.surface.fill(Color.WHITE)
            # BOX
            for y in range(0, 600, 50):
                pg.draw.line(self.surface, Color.GREY, (0, y), (800, y))
            for x in range(0, 800, 50):
                pg.draw.line(self.surface, Color.GREY, (x, 0), (x, 600))
            pg.draw.rect(self.surface, Color.BLACK, self.box_rect, self.box_thickness)
            # POINTS
            self.point_A.draw(self.surface)
            self.point_B.draw(self.surface)
            pg.draw.line(self.surface, Color.BLUE, self.point_A.get_pos(), self.point_B.get_pos(), 5)
            # VECTOR
            pg.display.flip()
            self.clock.tick(144)
if __name__ == "__main__":
    app = BounceTest()
    app.run()