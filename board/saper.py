from settings import (
    GREEN,
    YELLOW,
    RED,
)
from flag import (
    RedFlag,
    YellowFlag,
    GreenFlag,
)
from mine import BaseField
import pygame


class Saper(object):

    def __init__(self, grid_quan, name, grid, flag_grid):
        self.grid = grid
        self.flag_grid = flag_grid
        self.grid_quan = grid_quan - 1
        self.img = pygame.image.load('board/saper.png')
        self.coords = [grid_quan-1, grid_quan-1]
        self.name = name
        self.health = 100
        self.current_flag_colour = GREEN

    def no_flag(self):
        self.current_flag_colour = 0
        return 0

    def red_flag(self):
        self.current_flag_colour = RED
        return RED

    def yellow_flag(self):
        self.current_flag_colour = YELLOW
        return YELLOW

    def green_flag(self):
        self.current_flag_colour = GREEN
        return GREEN

    def left(self):
        if self.coords[1] > 0:
            self.coords[1] -= 1

    def right(self):
        if self.coords[1] < self.grid_quan:
            self.coords[1] += 1

    def up(self):
        if self.coords[0] > 0:
            self.coords[0] -= 1

    def down(self):
        if self.coords[0] < self.grid_quan:
            self.coords[0] += 1

    def place_flag_left(self):
        if self.coords[1] > 0:
            self._place_flag([self.coords[0], self.coords[1] - 1])

    def place_flag_right(self):
        if self.coords[1] < self.grid_quan-1:
            self._place_flag([self.coords[0], self.coords[1] + 1])

    def place_flag_up(self):
        if self.coords[0] > 0:
            self._place_flag([self.coords[0] - 1, self.coords[1]])

    def place_flag_down(self):
        if self.coords[0] < self.grid_quan-1:
            self._place_flag([self.coords[0] + 1, self.coords[1]])

    def _place_flag(self, coords):
        if self.current_flag_colour == 0:
            self.remove_flag(coords)
        elif self.flag_grid[coords[0]][coords[1]] == 0 and self.no_of_flags > 0:
            if self.current_flag_colour == GREEN:
                flag = GreenFlag(coords)
            elif self.current_flag_colour == YELLOW:
                flag = YellowFlag(coords)
            elif self.current_flag_colour == RED:
                flag = RedFlag(coords)
            self.flag_grid[coords[0]][coords[1]] = flag
            self.no_of_flags -= 1

    def remove_flag(self, coords):
        if self.flag_grid[coords[0]][coords[1]] != 0:
            self.no_of_flags += 1
            self.flag_grid[coords[0]][coords[1]] = 0

    def detonate(self):
        detonated_mines = 0
        for y in xrange(self.grid_quan + 1):
            for x in xrange(self.grid_quan + 1):
                if self.flag_grid[x][y]:
                    if self.flag_grid[x][y].color == self.grid[x][y].color:
                        self.grid[x][y] = BaseField()
                        detonated_mines += 1
                    self.flag_grid[x][y] = 0
        return detonated_mines

    def reset_position(self):
        self.coords = [self.grid_quan, self.grid_quan]
