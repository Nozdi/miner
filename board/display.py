from settings import CELL, GREY, BLACK, WHITE, RED, YELLOW, GREEN
import pygame
from random import randint
from mine import *


class Display(object):
    def __init__(self, quantity):
        self.quantity = quantity
        self.menu_height = 50
        self.width = self.size_by_name('width')
        self.height = self.size_by_name('height') + self.menu_height
        self.grid = [[0 for r in xrange(self.quantity)] for c in xrange(self.quantity)]

        self.place_mines(quantity, 10)  # 10 is a number of mines

        self.title = "Miner"
        self.saper = Saper(quantity, "player")  # use here your bot name
        self.done = False

        self.initialize_pygame()

    def size_by_name(self, name):
        return self.quantity * (CELL[name] + CELL['margin']) + CELL['margin']

    def initialize_pygame(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

        self.clock = pygame.time.Clock()

        pygame.font.init()
        self.font = pygame.font.SysFont("comicsansms", max(self.quantity * 2/3, 10))

    def place_mine(self, grid_quan):
        position = (randint(0, grid_quan-1), randint(0, grid_quan-1))
        scheme_number = randint(1, 511)
        number = randint(1, 3)
        mine_type = {
            1: GreenMine,
            2: YellowMine,
            3: RedMine
        }[number]
        scheme = Scheme(scheme_number, mine_type)
        absolute_pos = scheme.get_absolute_pos(*position)
        mines = scheme.fetch_mines(*position)
        for pos in absolute_pos:
            try:
                if self.grid[pos[0]][pos[1]] != 0:
                    return False
            except IndexError:
                return False

            try:
                if self.grid[pos[0]+1][pos[1]] == number:
                    return False
            except IndexError:
                pass

            try:
                if self.grid[pos[0]-1][pos[1]] == number:
                    return False
            except IndexError:
                pass

            try:
                if self.grid[pos[0]][pos[1]+1] == number:
                    return False
            except IndexError:
                pass

            try:
                if self.grid[pos[0]][pos[1]-1] == number:
                    return False
            except IndexError:
                pass

        for pos in absolute_pos:
            self.grid[pos[0]][pos[1]] = number
        return True

    def place_mines(self, grid_quan, number_of_mines):
        while number_of_mines > 0:
            while not self.place_mine(grid_quan):
                pass
            number_of_mines -= 1

    def debug_grid(self):
        for row in xrange(self.quantity):
            for column in xrange(self.quantity):
                rect = pygame.Rect(
                    (CELL['margin'] + CELL['width']) * column + CELL['margin'],
                    ((CELL['margin'] + CELL['height']) * row
                        + CELL['margin'] + self.menu_height),
                    CELL['width'], CELL['height']
                )
                color = {
                    0: WHITE,
                    1: GREEN,
                    2: YELLOW,
                    3: RED
                }[self.grid[row][column]]
                pygame.draw.rect(self.screen, color, rect)
                if [row, column] == self.saper.cords:
                    self.screen.blit(self.saper.img, rect)

    def draw_grid(self):
        for row in xrange(self.quantity):
            for column in xrange(self.quantity):
                rect = pygame.Rect(
                    (CELL['margin'] + CELL['width']) * column + CELL['margin'],
                    ((CELL['margin'] + CELL['height']) * row
                        + CELL['margin'] + self.menu_height),
                    CELL['width'], CELL['height']
                )
                pygame.draw.rect(self.screen, WHITE, rect)
                if [row, column] == self.saper.cords:
                    self.screen.blit(self.saper.img, rect)

    def draw_menu(self):
        menu_rect = pygame.Rect(0, 0, self.width, self.menu_height)
        pygame.draw.rect(self.screen, GREY, menu_rect)

        name = self.font.render("Name: {}".format(self.saper.name), True, BLACK)
        self.screen.blit(name, (self.width/50, 1))

        current_health = self.font.render(
            "Health: {}".format(self.saper.health), True, RED
            )
        self.screen.blit(current_health, (self.width/50, 25))

        meters = self.font.render("Meters: ", True, BLACK)
        self.screen.blit(meters, (self.width*0.35, 13))
        wpos = self.width/2
        for color in (RED, YELLOW, GREEN):
            meter = self.font.render("{} %".format(100), True, color)
            self.screen.blit(meter, (wpos, 13))
            wpos += self.width/7

    def run(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.saper.left()
                    elif event.key == pygame.K_RIGHT:
                        self.saper.right()
                    elif event.key == pygame.K_UP:
                        self.saper.up()
                    if event.key == pygame.K_DOWN:
                        self.saper.down()

            self.screen.fill(BLACK)

            # draw here
            #self.draw_grid()
            self.debug_grid()
            self.draw_menu()

            pygame.display.flip()

            self.clock.tick(20)
        pygame.quit()


class Saper(object):

    def __init__(self, grid_quan, name):
        self.grid_quan = grid_quan - 1
        self.img = pygame.image.load('board/saper.png')
        self.cords = [grid_quan-1, grid_quan-1]
        self.name = name
        self.health = 100

    def left(self):
        if self.cords[1] > 0:
            self.cords[1] -= 1

    def right(self):
        if self.cords[1] < self.grid_quan:
            self.cords[1] += 1

    def up(self):
        if self.cords[0] > 0:
            self.cords[0] -= 1

    def down(self):
        if self.cords[0] < self.grid_quan:
            self.cords[0] += 1
