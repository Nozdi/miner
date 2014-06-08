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
from mine import (
    Scheme,
    BaseField,
    GreenMine,
    YellowMine,
    RedMine,
)
from flag import (
    Flag,
    RedFlag,
    YellowFlag,
    GreenFlag,
)
from random import sample, randint
import pygame
from copy import deepcopy
from time import sleep
from saper import Saper


class Display(object):

    def __init__(self, quantity):
        self.quantity = quantity
        self.menu_height = 50
        self.gameover_height = 50
        self.width = self.size_by_name('width')
        self.height = self.size_by_name('height') + self.menu_height
        self.grid = [[0 for r in xrange(self.quantity)]
                     for c in xrange(self.quantity)]

        self.title = "Miner"
        self.hide_mines = False
        self.done = False
        self.no_of_schemes = (self.quantity**2)/30
        self.no_of_mines = self.no_of_schemes*9
        self.schemes = [
            Scheme(no, mine) for no, mine in zip(
                sample(SCHEMES, 3), [GreenMine, YellowMine, RedMine])]
        self.place_mines()
        self.grid_copy = deepcopy(self.grid)
        self.saper = Saper(quantity, "player", self.grid_copy)
        self.saper.no_of_flags = round((self.no_of_schemes * 9)*1.5)
        self.compute_mines()
        self.compute_meters()
        self.initialize_pygame()

    def size_by_name(self, name):
        return self.quantity * (CELL[name] + CELL['margin']) + CELL['margin']

    def initialize_pygame(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

        self.clock = pygame.time.Clock()

        pygame.font.init()
        self.font = pygame.font.SysFont(
            "comicsansms", max(self.quantity * 2/3, 25))

    def place_mines(self):
        for scheme in self.schemes:
            no = (self.quantity**2)/30
            # no = round(self.quantity/1.8)
            while no > 0:
                while not scheme.place(self.grid):
                    continue
                no -= 1
        for row in xrange(self.quantity):
            for column in xrange(self.quantity):
                if self.grid[row][column] == 0:
                    self.grid[row][column] = BaseField()

    def reset_mines(self):
        for row in self.saper.grid:
            for mine in row:
                mine.reset_radiation()

    def compute_mines(self):
        self.reset_mines()
        for column in xrange(self.quantity):
            for row in xrange(self.quantity):
                field = self.saper.grid[row][column]
                if field.damage:
                    for i in xrange(-2, 3):
                        for j in xrange(-2, 3):
                            if (0 <= row+i < self.quantity
                               and 0 <= column+j < self.quantity):
                                (self.saper.grid[row+i][column+j].radiation[
                                    field.colour]).append(MINE_RANGE[2+i][2+j])

        for row in xrange(self.quantity):
            for column in xrange(self.quantity):
                self.saper.grid[row][column].compute_max()

    def compute_meters(self):
        x, y = self.saper.coords
        self.radiations = {
            RED: [0],
            YELLOW: [0],
            GREEN: [0],
        }
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= x+i < self.quantity and 0 <= y+j < self.quantity:
                    for key, val in self.saper.grid[x+i][y+j].max_radiation.items():
                        self.radiations[key].append(val)
        for key in self.radiations:
            self.radiations[key] = reduce(
                lambda x, y: x+y-x*y, self.radiations[key])
        self.saper.set_meters(self.radiations)

    def draw_grid(self):
        for row in xrange(self.quantity):
            for column in xrange(self.quantity):
                rect = pygame.Rect(
                    (CELL['margin'] + CELL['width']) * column + CELL['margin'],
                    ((CELL['margin'] + CELL['height']) * row
                        + CELL['margin'] + self.menu_height),
                    CELL['width'], CELL['height']
                )

                # if (self.saper.grid_knowledge[row][column] == 1):
                if (self.saper.grid_knowledge[row][column] == 0 and
                        self.saper.grid[row][column].colour != WHITE):
                    colour = BLACK
                else:
                    colour = self.saper.grid[row][column].colour
                if self.hide_mines:
                    colour = WHITE

                pygame.draw.rect(self.screen, colour, rect)

                if [row, column] == self.saper.coords:
                    self.screen.blit(self.saper.img, rect)
                if self.saper.flag_grid[row][column] != 0:
                    self.screen.blit(
                        self.saper.flag_grid[row][column].img, rect)

    def draw_menu(self):
        menu_rect = pygame.Rect(0, 0, self.width, self.menu_height)
        pygame.draw.rect(self.screen, GREY, menu_rect)

        name = self.font.render(
            "Name: {}".format(self.saper.name), True, BLACK
            )
        self.screen.blit(name, (self.width/50, 1))

        current_attempts = self.font.render(
            "Attempts: {}".format(self.saper.attempts), True, BLACK
            )
        self.screen.blit(current_attempts, (self.width*0.25, 25))

        current_flags = self.font.render(
            "Flags: {:.0f}".format(self.saper.no_of_flags), True, BLACK
            )
        self.screen.blit(current_flags, (self.width/2, 25))

        current_mines = self.font.render(
            "Mines: {}".format(self.no_of_mines), True, BLACK
            )
        self.screen.blit(current_mines, (self.width*0.75, 25))

        current_health = self.font.render(
            "Health: {}".format(self.saper.health), True, RED
            )
        self.screen.blit(current_health, (self.width/50, 25))

        meters = self.font.render("Meters: ", True, BLACK)
        self.screen.blit(meters, (self.width*0.35, 1))
        wpos = self.width/2

        self.compute_meters()
        for colour, value in self.radiations.items():
            meter = self.font.render(
                "{:.2f} %".format(value*100), True, colour)
            self.screen.blit(meter, (wpos, 1))
            wpos += self.width/7

    def draw_all(self):
        self.screen.fill(BLACK)
        self.draw_grid()

        if self.no_of_mines > 0:
            self.draw_menu()
        else:
            self.draw_gameover()
            sleep(2)
        pygame.display.flip()

    def draw_gameover(self):
        gameover_rect = pygame.Rect(0, 0, self.width, self.gameover_height)
        pygame.draw.rect(self.screen, GREY, gameover_rect)

        name = self.font.render("GAME OVER".format(), True, RED)
        self.screen.blit(name, (self.width/50, 1))

    def run(self):
        self.draw_all()
        while self.no_of_mines > 0:
            self.no_of_mines -= self.saper.detonate()
            self.compute_mines()
            self.saper.move()
            sleep(0.1)

            row, column = self.saper.coords

            self.saper.lose_health(self.saper.grid[row][column].damage)
            if self.saper.grid[row][column].damage > 0:
                self.saper.grid[row][column] = BaseField()
                self.no_of_mines -= 1
                self.compute_mines()

            if self.saper.health <= 0:
                self.saper.attempts += 1
                self.saper.reset_health()
                self.saper.reset_position()
                self.grid_copy = deepcopy(self.grid)
                self.saper.grid = self.grid_copy
                self.compute_mines()
                self.saper.flag_grid = [
                    [0 for r in xrange(
                        self.quantity)] for c in xrange(self.quantity)]
                self.saper.no_of_flags = round((self.no_of_schemes * 9)*1.5)
                self.no_of_mines = self.no_of_schemes * 9

            self.draw_all()

            self.clock.tick(20)

        pygame.quit()
