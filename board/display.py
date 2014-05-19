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
        self.hide_mines = False
        self.done = False
        self.current_flag_colour = GREEN
        self.no_of_schemes = (self.quantity**2)/30
        self.no_of_flags = round((self.no_of_schemes *3)*1.1)
        self.schemes = [Scheme(no, mine) for no, mine in
                        zip(sample(SCHEMES, 3), [GreenMine, YellowMine, RedMine])]
        self.place_mines()
        self.grid_copy = deepcopy(self.grid)
        self.compute_mines()
        self.compute_meters()
        self.flag_grid = [[0 for r in xrange(self.quantity)] for c in xrange(self.quantity)]
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

    def compute_mines(self):
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
        x, y = self.saper.cords
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

                if [row, column] == self.saper.cords:
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
            "Flags: {}".format(self.no_of_flags), True, BLACK
            )
        self.screen.blit(current_flags, (self.width/2, 25))

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

    def place_flag(self, colour, cords):
        if colour == 0:
            self.remove_flag(cords)
        elif self.flag_grid[cords[0]][cords[1]] == 0:
            if colour == GREEN:
                flag = GreenFlag(cords)
            elif colour == YELLOW:
                flag = YellowFlag(cords)
            elif colour == RED:
                flag = RedFlag(cords) 
            self.flag_grid[cords[0]][cords[1]] = flag
            self.no_of_flags -= 1

    def remove_flag(self, cords):
        if self.flag_grid[cords[0]][cords[1]] != 0:
            self.no_of_flags += 1
            self.flag_grid[cords[0]][cords[1]] = 0    

    def detonate(self):
        for y in xrange(self.quantity):
            for x in xrange(self.quantity):
                if self.flag_grid[x][y]:
                    if self.flag_grid[x][y].color == self.grid_copy[x][y].color:
                        self.grid_copy[x][y] = BaseField()
                    self.flag_grid[x][y] = 0 

    def run(self):
        self.draw_all()
        while self.lifes and not self.done:
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
                        self.current_flag_colour = 0
                    elif event.key == pygame.K_1:
                        self.current_flag_colour = GREEN
                    elif event.key == pygame.K_2:
                        self.current_flag_colour = YELLOW
                    elif event.key == pygame.K_3:
                        self.current_flag_colour = RED
                    elif event.key == pygame.K_q:
                        self.detonate()
                    elif event.key == pygame.K_w:
                        if self.saper.cords[0] > 0:
                            self.place_flag(self.current_flag_colour, [self.saper.cords[0] - 1, self.saper.cords[1]])
                    elif event.key == pygame.K_s:
                        if self.saper.cords[0] < self.quantity-1:
                            self.place_flag(self.current_flag_colour, [self.saper.cords[0] + 1, self.saper.cords[1]])
                    elif event.key == pygame.K_a:
                        if self.saper.cords[1] > 0:
                            self.place_flag(self.current_flag_colour, [self.saper.cords[0], self.saper.cords[1] - 1])
                    elif event.key == pygame.K_d:
                        if self.saper.cords[1] < self.quantity-1:
                            self.place_flag(self.current_flag_colour, [self.saper.cords[0], self.saper.cords[1] + 1])

                    row, column = self.saper.cords

                    self.saper.health -= self.grid_copy[row][column].damage

                    if self.saper.health <= 0:
                        self.lifes -= 1
                        self.saper.health = 100
                        self.saper.reset_position()
                        self.grid_copy = deepcopy(self.grid)
                        self.flag_grid = [[0 for r in xrange(self.quantity)] for c in xrange(self.quantity)]
                        self.no_of_flags = round((self.no_of_schemes *3)*1.1)

                    self.draw_all()

            self.clock.tick(20)

        sleep(2)
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
