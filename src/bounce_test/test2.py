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

NAME = "Box-Point Vector Problem Simulation"

class Game:
    def decorate_window(self) -> None:
        pg.display.set_caption(NAME)
        pg.display.set_icon(pg.Surface((0,0)))
    def __init__(self) -> None:
        self.surface = pg.display.set_mode((800, 600), pg.NOFRAME | pg.HIDDEN)
        self.configure_events()
        self.decorate_window()
        self.create_grid_surface()
        self.setup()
        self.clock = pg.time.Clock()
    def setup(self) -> None:
        self.lines = ((200, 200), (600, 200)), ((200, 200), (200, 400)), ((600, 200), (600, 400)), ((200, 400), (600, 400))
        self.lines_bp = (200, 200), (600, 200), (600, 400), (200, 400)
    def create_grid_surface(self) -> None:
        self.grid_surface = pg.Surface((800, 600))
        self.grid_surface.fill(Color.WHITE)
        for x in range(0, 800, 50):
            pg.draw.line(self.grid_surface, Color.GREY, (x, 0), (x, 600))
        for y in range(0, 600, 50):
            pg.draw.line(self.grid_surface, Color.GREY, (0, y), (800, y))
    def configure_events(self) -> None:
        pg.event.set_blocked(None)
        pg.event.set_allowed((pg.MOUSEMOTION, pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP, pg.QUIT, pg.KEYUP, pg.KEYDOWN))
    def quit(self) -> None:
        pg.quit()
        sys.exit()
    def show_window(self) -> None:
        self.surface = pg.display.set_mode((800, 600), pg.NOFRAME | pg.SHOWN)
    def return_refl(self, point, intersection, line):
        #print(point)
        if line == self.lines[0] or line == self.lines[3]:
            return (point[0], intersection[1] - (point[1] - intersection[1]))
        else:
            return (intersection[0] - (point[0] - intersection[0]), point[1])
    def get_points(self, n, start, end, last_line):
        inter_x_y = None
        for line in self.lines:
            inter_x_y = self.segment_intersection((start, end), line)
            if inter_x_y != None and line != last_line:
                last_line = line
                break
        if inter_x_y == None:
            print("NO INTER")
            pg.draw.line(self.surface, Color.BLACK, start, end)
        elif n == 0:
            print("N = 0")
            pg.draw.line(self.surface, Color.BLACK, start, inter_x_y)
        else:
            refl_point = self.return_refl(end, inter_x_y, last_line)
            pg.draw.line(self.surface, Color.BLACK, start, inter_x_y)
            self.get_points(n-1, inter_x_y, refl_point, last_line)
    def run(self) -> None:
        self.pts = []
        self.show_window() # avoid the blank screen at the start
        self.mouse_x, self.mouse_y = 300, 400
        while 1:
            for event in pg.event.get():
                #print(event)
                match event.type:
                    case pg.QUIT:
                        self.quit()
                    case pg.KEYDOWN:
                        match event.key:
                            case 27:
                                self.quit()
                    case pg.MOUSEMOTION:
                        self.mouse_x,self.mouse_y=event.pos
            # ALWAYS HERE
            self.surface.blit(self.grid_surface, (0, 0))
            pg.draw.lines(self.surface, Color.BLACK, True, self.lines_bp)
            a = (400, 300)
            b = (self.mouse_x, self.mouse_y)
            d = pg.Vector2(b[0]-a[0], b[1]-a[1])
            d.scale_to_length(1000)
            c = int(d.x), int(d.y)
            inter_1 = None
            for line in self.lines:
                inter_1 = self.segment_intersection((a, c), line)
                if inter_1 != None:
                    da_line = line
                    break
            if inter_1 != None:
                refl = self.return_refl(c, inter_1, da_line)
                pg.draw.line(self.surface, Color.BLUE, a, inter_1)
                pg.draw.line(self.surface, Color.RED, inter_1, refl)
                a = inter_1
                c = refl
                inter_1 = None
                for line in self.lines:
                    inter_1 = self.segment_intersection((a, c), line)
                    if inter_1 != None:
                        da_line = line
                        break
                if inter_1 != None:
                    refl = self.return_refl(c, inter_1, da_line)
                    pg.draw.line(self.surface, Color.BLACK, inter_1, refl)
                    a = inter_1
                    c = refl
            pg.display.flip()
            self.clock.tick_busy_loop()

    def segment_intersection(self, segment1, segment2):
        xdiff = (segment1[0][0] - segment1[1][0], segment2[0][0] - segment2[1][0])
        ydiff = (segment1[0][1] - segment1[1][1], segment2[0][1] - segment2[1][1])
        
        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            return None

        d = (det(*segment1), det(*segment2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div

        if (segment1[0][0] <= x <= segment1[1][0] or segment1[1][0] <= x <= segment1[0][0]) and \
        (segment1[0][1] <= y <= segment1[1][1] or segment1[1][1] <= y <= segment1[0][1]) and \
        (segment2[0][0] <= x <= segment2[1][0] or segment2[1][0] <= x <= segment2[0][0]) and \
        (segment2[0][1] <= y <= segment2[1][1] or segment2[1][1] <= y <= segment2[0][1]):
            return int(x), int(y)
        return None

if __name__ == "__main__":
    app = Game()
    app.run()