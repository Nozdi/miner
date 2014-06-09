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
from saper import Saper
from random import sample
import pygame
from copy import deepcopy
from time import sleep
from bot import Bot


class Display(object):

    def __init__(self, quantity):
        self.quantity = quantity
        self.menu_height = 50
        self.gameover_height = 50
        self.width = self.size_by_name('width')
        self.height = self.size_by_name('height') + self.menu_height
        self.grid = [[0 for r in xrange(self.quantity)] for c in xrange(self.quantity)]

        self.title = "Miner"
        self.lifes = 3          # put here number of lifes for miner
        self.hide_mines = False
        self.done = False
        self.no_of_schemes = (self.quantity**2)/30
        self.no_of_mines = self.no_of_schemes*9
        #self.no_of_flags = round((self.no_of_schemes *9)*1.1)
        self.schemes = [Scheme(no, mine) for no, mine in
                        zip(sample(SCHEMES, 3), [GreenMine, YellowMine, RedMine])]
        self.place_mines()
        self.grid_copy = deepcopy(self.grid)
        self.flag_grid = [[0 for r in xrange(self.quantity)] for c in xrange(self.quantity)]
        self.saper = Saper(quantity, "Symbolic_bot", self.grid_copy, self.flag_grid)
        self.saper.no_of_flags = round((self.no_of_schemes * 9)*1.7)

        #bot
        self.bot_mode = False
        self.bot = Bot(self.saper, self)

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
        self.font = pygame.font.SysFont("comicsansms", max(self.quantity * 2/3, 15))

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
        for row in self.grid_copy:
            for mine in row:
                mine.reset_radiation()

    def compute_mines(self):
        self.reset_mines()
        for column in xrange(self.quantity):
            for row in xrange(self.quantity):
                field = self.grid_copy[row][column]
                if field.damage:
                   for i in xrange(-2, 3):
                        for j in xrange(-2, 3):
                            if 0 <= row+i < self.quantity and 0 <= column+j < self.quantity:
                                (self.grid_copy[row+i][column+j].radiation[field.color]
                                    ).append(MINE_RANGE[2+i][2+j])

        for row in xrange(self.quantity):
            for column in xrange(self.quantity):
                # print self.grid_copy[row][column].radiation
                self.grid_copy[row][column].compute_max()

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
                    for key, val in self.grid_copy[x+i][y+j].max_radiation.items():
                        self.radiations[key].append(val)
        for key in self.radiations:
            self.radiations[key] = reduce(lambda x,y: x+y-x*y, self.radiations[key])

    def draw_grid(self):
        for row in xrange(self.quantity):
            for column in xrange(self.quantity):
                rect = pygame.Rect(
                    (CELL['margin'] + CELL['width']) * column + CELL['margin'],
                    ((CELL['margin'] + CELL['height']) * row
                        + CELL['margin'] + self.menu_height),
                    CELL['width'], CELL['height']
                )

                color = self.grid_copy[row][column].color
                if self.hide_mines:
                    color = WHITE

                pygame.draw.rect(self.screen, color, rect)

                if [row, column] == self.saper.coords:
                    self.screen.blit(self.saper.img, rect)
                if self.flag_grid[row][column] != 0:
                    self.screen.blit(self.flag_grid[row][column].img, rect)

    def draw_menu(self):
        menu_rect = pygame.Rect(0, 0, self.width, self.menu_height)
        pygame.draw.rect(self.screen, GREY, menu_rect)

        name = self.font.render("Name: {}".format(self.saper.name), True, BLACK)
        self.screen.blit(name, (self.width/50, 1))

        current_lifes = self.font.render(
            "Lifes: {}".format(self.lifes), True, BLACK
            )
        self.screen.blit(current_lifes, (self.width*0.35, 25))

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
        for color, value in self.radiations.items():
            meter = self.font.render("{:.2f} %".format(value*100), True, color)
            self.screen.blit(meter, (wpos, 1))
            wpos += self.width/7

    def draw_all(self):
        self.screen.fill(BLACK)
        self.draw_grid()

        if self.lifes > 0:
            self.draw_menu()
        else:
            self.draw_gameover()
        pygame.display.flip()

    def draw_gameover(self):
        gameover_rect = pygame.Rect(0, 0, self.width, self.gameover_height)
        pygame.draw.rect(self.screen, GREY, gameover_rect)

        name = self.font.render("GAME OVER".format(), True, RED)
        self.screen.blit(name, (self.width/50, 1))

    def game(self):
        row, column = self.saper.coords

        self.saper.health -= self.grid_copy[row][column].damage
        if self.grid_copy[row][column].damage > 0:
            self.grid_copy[row][column] = BaseField()
            self.no_of_mines -= 1
            self.compute_mines()

        if self.saper.health <= 0:
            self.lifes -= 1
            self.saper.health = 100
            self.saper.reset_position()
            self.grid_copy = deepcopy(self.grid)
            self.compute_mines()
            self.flag_grid = [[0 for r in xrange(self.quantity)]
                              for c in xrange(self.quantity)]
            self.saper.no_of_flags = round((self.no_of_schemes * 9)*1.7)
            self.no_of_mines = self.no_of_schemes * 9

        self.draw_all()

    def run(self):
        self.draw_all()
        while self.lifes and not self.done:
            if not self.bot_mode:
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
                        elif event.key == pygame.K_h:
                            self.hide_mines = not self.hide_mines
                        elif event.key == pygame.K_0:
                            self.saper.no_flag()
                        elif event.key == pygame.K_1:
                            self.saper.green_flag()
                        elif event.key == pygame.K_2:
                            self.saper.yellow_flag()
                        elif event.key == pygame.K_3:
                            self.saper.red_flag()
                        elif event.key == pygame.K_q:
                            self.no_of_mines -= self.saper.detonate()
                            self.compute_mines()
                        elif event.key == pygame.K_w:
                            self.saper.place_flag_up()
                        elif event.key == pygame.K_s:
                            self.saper.place_flag_down()
                        elif event.key == pygame.K_a:
                            self.saper.place_flag_left()
                        elif event.key == pygame.K_d:
                            self.saper.place_flag_right()
                        elif event.key == pygame.K_b:
                            self.bot_mode = True
                            self.bot_move = self.bot.run()
                        self.game()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                        self.bot_mode = False
                try:
                    next(self.bot_move)
                except StopIteration:
                    print("Bot nie wie co dalej :(")
                    print("Punkty bota: {}".format(self.bot.score))
                    break
                self.game()
            self.clock.tick(20)

        # sleep(2)
        pygame.quit()
