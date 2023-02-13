import pygame as pg
import numpy as np
import sys

sys.setrecursionlimit(2048)


class Color:
    WHITE = pg.Color(251, 251, 242)
    RED = pg.Color(255, 29, 21)
    GREEN = pg.Color(62, 195, 0)
    BLACK = pg.Color(35, 28, 7)
    GREY = pg.Color(200, 200, 200)
    BLUE = pg.Color(100, 100, 250)


NAME = "Box-Point Vector Problem Simulation"


class Game:
    def decorate_window(self) -> None:
        pg.display.set_caption(NAME)
        pg.display.set_icon(pg.Surface((0, 0)))

    def __init__(self) -> None:
        self.surface = pg.display.set_mode((800, 600), pg.NOFRAME | pg.HIDDEN)
        self.configure_events()
        self.decorate_window()
        self.create_grid_surface()
        self.setup()
        self.colors = [Color.RED, Color.GREEN, Color.BLACK, Color.GREY, Color.BLUE]
        self.clock = pg.time.Clock()

    def setup(self) -> None:
        self.lines = ((450, 500), (450, 250)), ((350, 100), (350, 350)), ((100, 100), (700, 100)), ((
            100, 100), (100, 500)), ((700, 100), (700, 500)), ((100, 500), (700, 500))

    def calc_dist(self, p1, p2):
        return (p2[0]-p1[0])**2+(p2[1]-p1[1])**2

    def create_grid_surface(self) -> None:
        self.grid_surface = pg.Surface((800, 600))
        self.grid_surface.fill(Color.WHITE)
        for x in range(0, 800, 50):
            pg.draw.line(self.grid_surface, Color.GREY, (x, 0), (x, 600))
        for y in range(0, 600, 50):
            pg.draw.line(self.grid_surface, Color.GREY, (0, y), (800, y))

    def configure_events(self) -> None:
        pg.event.set_blocked(None)
        pg.event.set_allowed((pg.MOUSEMOTION, pg.MOUSEBUTTONDOWN,
                             pg.MOUSEBUTTONUP, pg.QUIT, pg.KEYUP, pg.KEYDOWN))

    def quit(self) -> None:
        pg.quit()
        sys.exit()

    def show_window(self) -> None:
        self.surface = pg.display.set_mode((800, 600), pg.NOFRAME | pg.SHOWN)

    def return_refl(self, point, intersection, line):
        if line[1][1] - line[0][1] == 0:
            return (point[0], intersection[1] - (point[1] - intersection[1]))
        else:
            return (intersection[0] - (point[0] - intersection[0]), point[1])

    def get_points(self, n, start, end, last_line):
        inter_x_y = None
        for line in self.sort_list(start):
            inter_x_y = self.segment_intersection((start, end), line)
            if inter_x_y != None and line != last_line:
                last_line = line
                break
        color = self.color.lerp(Color.RED, 1 / self.n * n)
        if inter_x_y == None:
            pg.draw.aaline(self.surface, color, start, end)
        elif n == 0:
            pg.draw.aaline(self.surface, color, start, inter_x_y)
        else:
            refl_point = self.return_refl(end, inter_x_y, last_line)
            pg.draw.aaline(self.surface, color, start, inter_x_y)
            self.get_points(n-1, inter_x_y, refl_point, last_line)

    def sort_list(self, point):
        return sorted(self.lines, key=lambda a: self.calc_Ldist(a, point))

    def calc_Ldist(self, a, point):
        # a[0]=v
        len_2 = self.calc_dist(a[0], a[1])
        if (len_2 == 0):
            return self.calc_dist(a[0], point)
        t = max(0, min(1, self.dot(
            (point[0]-a[0][0], point[1]-a[0][1]), (a[0][0]-a[1][0], a[0][1]-a[1][1]))))
        proj = (a[0][0]+t*(a[1][0]-a[0][0]), a[0][1]+t*(a[1][1]-a[0][1]))
        return self.calc_dist(proj, point)

    def dot(self, v1, v2):
        return v1[0]*v2[0] - v1[1]*v2[0]

    def run(self) -> None:
        self.pts = []
        self.show_window()  # avoid the blank screen at the start
        self.mouse_x, self.mouse_y = 300, 400
        while 1:
            for event in pg.event.get():
                # print(event)
                match event.type:
                    case pg.QUIT:
                        self.quit()
                    case pg.KEYDOWN:
                        match event.key:
                            case 27:
                                self.quit()
                    case pg.MOUSEMOTION:
                        self.mouse_x, self.mouse_y = event.pos
            # ALWAYS HERE
            self.surface.blit(self.grid_surface, (0, 0))
            for line in self.lines:
                pg.draw.aaline(self.surface, Color.BLACK, line[0], line[1])
            a = (200, 300)
            b = (self.mouse_x, self.mouse_y)
            d = pg.Vector2(b[0]-a[0], b[1]-a[1]) 
            d.scale_to_length(10000)
            c = int(d.x+a[0]), int(d.y+a[1])
            self.n = 4
            self.color = Color.BLUE
            self.get_points(self.n, a, c, None)
            pg.display.flip()
            self.clock.tick_busy_loop()

    def segment_intersection(self, segment1, segment2):
        xdiff = (segment1[0][0] - segment1[1][0],
                 segment2[0][0] - segment2[1][0])
        ydiff = (segment1[0][1] - segment1[1][1],
                 segment2[0][1] - segment2[1][1])

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
