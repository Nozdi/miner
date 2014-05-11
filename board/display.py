from settings import (
    SCHEMES,
    CELL,
    GREY,
    BLACK,
    RED,
    YELLOW,
    GREEN,
    WHITE,
)
from mine import (
    Scheme,
    BaseField,
    GreenMine,
    YellowMine,
    RedMine,
)
from random import sample, randint
import pygame
from copy import deepcopy


class Display(object):

    def __init__(self, quantity):
        self.quantity = quantity
        self.menu_height = 50
        self.gameover_height = 50
        self.width = self.size_by_name('width')
        self.height = self.size_by_name('height') + self.menu_height
        self.grid = [[0 for r in xrange(self.quantity)] for c in xrange(self.quantity)]

        self.title = "Miner"
        self.saper = Saper(quantity, "player")  # use here your bot name
        self.lifes = 3          # put here number of lifes for miner
        self.done = False
        self.hide_mines = False

        self.schemes = [Scheme(no, mine) for no, mine in
                        zip(sample(SCHEMES, 3), [GreenMine, YellowMine, RedMine])]
        self.place_mines()
        self.grid_copy = deepcopy(self.grid)

        self.initialize_pygame()

    def size_by_name(self, name):
        return self.quantity * (CELL[name] + CELL['margin']) + CELL['margin']

    def initialize_pygame(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

        self.clock = pygame.time.Clock()

        pygame.font.init()
        self.font = pygame.font.SysFont("comicsansms", max(self.quantity * 2/3, 15))

    def place_mines(self):
        for scheme in self.schemes:
            # no = (self.quantity**2)/20
            no = round(self.quantity/1.5)
            while no > 0:
                while not scheme.place(self.grid):
                    continue
                no -= 1

    def draw_grid(self):
        for row in xrange(self.quantity):
            for column in xrange(self.quantity):
                rect = pygame.Rect(
                    (CELL['margin'] + CELL['width']) * column + CELL['margin'],
                    ((CELL['margin'] + CELL['height']) * row
                        + CELL['margin'] + self.menu_height),
                    CELL['width'], CELL['height']
                )
                if self.grid[row][column] == 0:
                    self.grid[row][column] = BaseField()

                color = self.grid[row][column].color
                if self.hide_mines:
                    color = WHITE

                pygame.draw.rect(self.screen, color, rect)

                if [row, column] == self.saper.cords:
                    self.screen.blit(self.saper.img, rect)

    def draw_menu(self):
        menu_rect = pygame.Rect(0, 0, self.width, self.menu_height)
        pygame.draw.rect(self.screen, GREY, menu_rect)

        name = self.font.render("Name: {}".format(self.saper.name), True, BLACK)
        self.screen.blit(name, (self.width/50, 1))

        current_lifes = self.font.render(
            "Lifes: {}".format(self.lifes), True, BLACK
            )
        self.screen.blit(current_lifes, (self.width/2, 35))

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

    def draw_gameover(self):
        gameover_rect = pygame.Rect(0, 0, self.width, self.gameover_height)
        pygame.draw.rect(self.screen, GREY, gameover_rect)

        name = self.font.render("GAME OVER".format(), True, RED)
        self.screen.blit(name, (self.width/50, 1))

    def compute_readout(self):
        x, y = self.saper.cords

    def run(self):
        while not self.done and self.lifes > 0:
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
                    elif event.key == pygame.K_DOWN:
                        self.saper.down()

                    row, column = self.saper.cords
                    self.saper.health -= self.grid[row][column].damage
                    if self.saper.health <= 0:
                        self.lifes -= 1
                        self.saper.health = 100
                        self.saper.reset_position()
                        self.grid_copy = deepcopy(self.grid)
                    
            self.screen.fill(BLACK)

            # draw here
            self.draw_grid()
            if self.lifes > 0:
                self.draw_menu()
            else:
                self.draw_gameover()

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

    def reset_position(self):
        self.cords = [self.grid_quan, self.grid_quan]
