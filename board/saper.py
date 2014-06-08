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
from math import sqrt


class Saper(object):

    def __init__(self, grid_quan, name, grid):
        self.grid = grid
        self.grid_quan = grid_quan - 1
        self.flag_grid = [[0 for r in xrange(self.grid_quan+1)]
                          for c in xrange(self.grid_quan+1)]
        self.img = pygame.image.load('board/saper.png')
        self.coords = [grid_quan-1, grid_quan-1]
        self.name = name
        self.MAX_HEALTH = 200
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

    def direction(self, name):
        if name == 'left':
            return self.left()
        elif name == 'right':
            return self.right()
        elif name == 'up':
            return self.up()
        elif name == 'down':
            return self.down()

    def left(self):
        return [self.coords[0], self.coords[1] - 1]

    def right(self):
        return [self.coords[0], self.coords[1] + 1]

    def up(self):
        return [self.coords[0] - 1, self.coords[1]]

    def down(self):
        return [self.coords[0] + 1, self.coords[1]]

    def go_left(self):
        if self.coords[1] > 0:
            self.coords[1] -= 1

    def go_right(self):
        if self.coords[1] < self.grid_quan + 1:
            self.coords[1] += 1

    def go_up(self):
        if self.coords[0] > 0:
            self.coords[0] -= 1

    def go_down(self):
        if self.coords[0] < self.grid_quan+1:
            self.coords[0] += 1

    def place_flag(self, coords):
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

    def remove_flag(self, coords):
        if self.flag_grid[coords[0]][coords[1]] != 0:
            self.no_of_flags += 1
            self.flag_grid[coords[0]][coords[1]] = 0

    def check(self, direction):
        return self.knowledge_copy[direction[0]][direction[1]]

    def check_go_left(self):
        if self.coords[1] > 0:
            if self.check(self.left()) < 1:
                return self.visited[self.coords[0]][self.coords[1]-1]
        return float('inf')

    def check_go_right(self):
        if self.coords[1]+1 < self.grid_quan + 1:
            if self.check(self.right()) < 1:
                return self.visited[self.coords[0]][self.coords[1]+1]
        return float('inf')

    def check_go_up(self):
        if self.coords[0] > 0:
            if self.check(self.up()) < 1:
                return self.visited[self.coords[0]-1][self.coords[1]]
        return float('inf')

    def check_go_down(self):
        if self.coords[0]+1 < self.grid_quan + 1:
            if self.check(self.down()) < 1:
                return self.visited[self.coords[0]+1][self.coords[1]]
        return float('inf')

    def check_mine(self, direction):
        if (self.coords[1] > 0
                and self.coords[1]+1 < self.grid_quan
                and self.coords[0] > 0
                and self.coords[0]+1 < self.grid_quan):
            if self.check(direction) == 1:
                return True
        return False

    def check_mine_left(self):
        if self.coords[1] > 0:
            if self.check(self.left()) == 1:
                return True
        return False

    def check_mine_right(self):
        if self.coords[1]+1 < self.grid_quan:
            if self.check(self.right()) == 1:
                return True
        return False

    def check_mine_up(self):
        if self.coords[0] > 0:
            if self.check(self.up()) == 1:
                return True
        return False

    def check_mine_down(self):
        if self.coords[0]+1 < self.grid_quan:
            if self.check(self.down()) == 1:
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

        neighbour_mines = {'left': self.check_mine_left(),
                           'right': self.check_mine_right(),
                           'up': self.check_mine_up(),
                           'down': self.check_mine_down()}

        v1 = list(self.meters.values())
        k1 = list(self.meters.keys())
        self.current_flag_colour = k1[v1.index(max(v1))]

        for key, value in neighbour_mines.iteritems():
            if value:
                self.place_flag(self.direction(key))

        neighbour_value = {'left': (self.check_go_left() +
                                    self.calculate_distance(self.left())),
                           'right': (self.check_go_right() +
                                     self.calculate_distance(self.right())),
                           'up': (self.check_go_up() +
                                  self.calculate_distance(self.up())),
                           'down': (self.check_go_down() +
                                    self.calculate_distance(self.down()))}

        v2 = list(neighbour_value.values())
        k2 = list(neighbour_value.keys())
        direction = k2[v2.index(min(v2))]
        if direction == 'left':
            self.go_left()
        elif direction == 'right':
            self.go_right()
        elif direction == 'up':
            self.go_up()
        elif direction == 'down':
            self.go_down()

    def am_i_on_mine(self):
        return self.health != self.old_health

    def set_meters(self, meters):
        self.meters = meters

    def calculate_distance(self, coords):
        min_distance = float('inf')
        for y in xrange(self.grid_quan + 1):
            for x in xrange(self.grid_quan + 1):
                if self.knowledge_copy[x][y] > 0:
                    distance = sqrt((x-coords[0])**2 + (y-coords[1])**2)
                    if distance < min_distance:
                        min_distance = distance
        return min_distance
