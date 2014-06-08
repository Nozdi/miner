import pygame
from time import sleep
from copy import deepcopy
from settings import (
    SCHEMES,
    CELL,
    GREY,
    BLACK,
    RED,
    YELLOW,
    GREEN,
    WHITE,
    MINE_RANGE,
)
from flag import (
    Flag,
    RedFlag,
    YellowFlag,
    GreenFlag,
)
from mine import (
    Scheme,
    BaseField,
    GreenMine,
    YellowMine,
    RedMine,
)


class Saper(object):

    def __init__(self, grid_quan, name, grid):
        self.grid = grid
        self.grid_quan = grid_quan - 1
        self.flag_grid = [[0 for r in xrange(self.grid_quan+1)]
                          for c in xrange(self.grid_quan+1)]
        self.img = pygame.image.load('board/saper.png')
        self.coords = [grid_quan-1, grid_quan-1]
        self.name = name
        self.MAX_HEALTH = 1000
        self.health = self.MAX_HEALTH
        self.old_health = self.MAX_HEALTH
        self.attempts = 0
        self.current_flag_colour = GREEN
        self.grid_knowledge = [[0.5 for r in xrange(self.grid_quan + 1)]
                               for c in xrange(self.grid_quan + 1)]
        self.knowledge_copy = [[0.5 for r in xrange(self.grid_quan + 1)]
                               for c in xrange(self.grid_quan + 1)]
        self.visited = [[0 for r in xrange(self.grid_quan + 1)]
                        for c in xrange(self.grid_quan + 1)]

    def left(self):
        if self.coords[1] > 0:
            self.coords[1] -= 1

    def right(self):
        if self.coords[1] < self.grid_quan + 1:
            self.coords[1] += 1

    def up(self):
        if self.coords[0] > 0:
            self.coords[0] -= 1

    def down(self):
        if self.coords[0] < self.grid_quan+1:
            self.coords[0] += 1

    def place_flag_left(self):
        self._place_flag([self.coords[0], self.coords[1] - 1])

    def place_flag_right(self):
        self._place_flag([self.coords[0], self.coords[1] + 1])

    def place_flag_up(self):
        self._place_flag([self.coords[0] - 1, self.coords[1]])

    def place_flag_down(self):
        self._place_flag([self.coords[0] + 1, self.coords[1]])

    def _place_flag(self, coords):
        if self.current_flag_colour == 0:
            self.remove_flag(coords)
        elif (self.flag_grid[coords[0]][coords[1]] == 0
              and self.no_of_flags > 0):
            if self.current_flag_colour == GREEN:
                flag = GreenFlag(coords)
            elif self.current_flag_colour == YELLOW:
                flag = YellowFlag(coords)
            elif self.current_flag_colour == RED:
                flag = RedFlag(coords)
            self.flag_grid[coords[0]][coords[1]] = flag
            self.no_of_flags -= 1

    def place_flag_direction(self, direction):
        if direction == 'left':
            self.place_flag_left()
        elif direction == 'right':
            self.place_flag_right()
        elif direction == 'up':
            self.place_flag_up()
        elif direction == 'down':
            self.place_flag_down()

    def remove_flag(self, coords):
        if self.flag_grid[coords[0]][coords[1]] != 0:
            self.no_of_flags += 1
            self.flag_grid[coords[0]][coords[1]] = 0

    def check_left(self):
        return self.knowledge_copy[self.coords[0]][self.coords[1] - 1]

    def check_right(self):
        return self.knowledge_copy[self.coords[0]][self.coords[1] + 1]

    def check_up(self):
        return self.knowledge_copy[self.coords[0] - 1][self.coords[1]]

    def check_down(self):
        return self.knowledge_copy[self.coords[0] + 1][self.coords[1]]

    def check_go_left(self):
        if self.coords[1] > 0:
            if self.check_left() < 1:
                return self.visited[self.coords[0]][self.coords[1]-1]
        return float('inf')

    def check_go_right(self):
        if self.coords[1]+1 < self.grid_quan + 1:
            if self.check_right() < 1:
                return self.visited[self.coords[0]][self.coords[1]+1]
        return float('inf')

    def check_go_up(self):
        if self.coords[0] > 0:
            if self.check_up() < 1:
                return self.visited[self.coords[0]-1][self.coords[1]]
        return float('inf')

    def check_go_down(self):
        if self.coords[0]+1 < self.grid_quan + 1:
            if self.check_down() < 1:
                return self.visited[self.coords[0]+1][self.coords[1]]
        return float('inf')

    def check_mine_left(self):
        if self.coords[1] > 0:
            if self.check_left() == 1:
                return True
        return False

    def check_mine_right(self):
        if self.coords[1]+1 < self.grid_quan:
            if self.check_right() == 1:
                return True
        return False

    def check_mine_up(self):
        if self.coords[0] > 0:
            if self.check_up() == 1:
                return True
        return False

    def check_mine_down(self):
        if self.coords[0]+1 < self.grid_quan:
            if self.check_down() == 1:
                return True
        return False

    def detonate(self):
        detonated_mines = 0
        for y in xrange(self.grid_quan + 1):
            for x in xrange(self.grid_quan + 1):
                if self.flag_grid[x][y]:
                    if self.flag_grid[x][y].colour == self.grid[x][y].colour:
                        self.grid[x][y] = BaseField()
                        detonated_mines += 1
                        self.knowledge_copy[x][y] = 0
                    self.flag_grid[x][y] = 0
        return detonated_mines

    def reset_position(self):
        self.coords = [self.grid_quan, self.grid_quan]

    def reset_health(self):
        self.health = self.MAX_HEALTH
        self.old_health = self.MAX_HEALTH
        self.knowledge_copy = deepcopy(self.grid_knowledge)

    def lose_health(self, damage):
        self.old_health = self.health
        self.health -= damage

    def move(self):
        if self.visited[self.coords[0]][self.coords[1]] == 0:
            if self.am_i_on_mine():
                self.grid_knowledge[self.coords[0]][self.coords[1]] = 1
            else:
                self.grid_knowledge[self.coords[0]][self.coords[1]] = 0
        self.visited[self.coords[0]][self.coords[1]] += 1
        self.knowledge_copy[self.coords[0]][self.coords[1]] = 0

        neighbour_value = {'left': self.check_go_left(),
                           'right': self.check_go_right(),
                           'up': self.check_go_up(),
                           'down': self.check_go_down()}

        neighbour_mines = {'left': self.check_mine_left(),
                           'right': self.check_mine_right(),
                           'up': self.check_mine_up(),
                           'down': self.check_mine_down()}

        v1 = list(self.meters.values())
        k1 = list(self.meters.keys())
        self.current_flag_colour = k1[v1.index(max(v1))]

        for key, value in neighbour_mines.iteritems():
            if value:
                self.place_flag_direction(key)
        v2 = list(neighbour_value.values())
        k2 = list(neighbour_value.keys())
        direction = k2[v2.index(min(v2))]
        if direction == 'left':
            self.left()
        elif direction == 'right':
            self.right()
        elif direction == 'up':
            self.up()
        elif direction == 'down':
            self.down()

    def am_i_on_mine(self):
        return self.health != self.old_health

    def set_meters(self, meters):
        self.meters = meters