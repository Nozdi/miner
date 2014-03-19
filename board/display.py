import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


CELL = {
    "width": 20,
    "height": 20,
    "margin": 5,
}


class Display(object):
    def __init__(self, quantity):
        self.quantity = quantity
        self.width = self.size_by_name('width')
        self.height = self.size_by_name('height')
        self.grid = [[0 for r in xrange(self.quantity)] for c in xrange(self.quantity)]
        self.title = "Miner"
        self.done = False
        self.saper = Saper(quantity)

    def size_by_name(self, name):
        return self.quantity * (CELL[name] + CELL['margin']) + CELL['margin']

    # def create_grid(self):
    #     self.grid = []
    #     for row in xrange(self.quantity):
    #         self.grid.append([])
    #         for column in xrange(self.quantity):
    #             self.grid[row].append(0)

    def initialize_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()

    def draw_grid(self):
        self.screen.fill(BLACK)
        for row in xrange(self.quantity):
            for column in xrange(self.quantity):
                rect = pygame.Rect(
                    (CELL['margin'] + CELL['width']) * column + CELL['margin'],
                    (CELL['margin'] + CELL['height']) * row + CELL['margin'],
                    CELL['width'], CELL['height']
                )
                pygame.draw.rect(self.screen, WHITE, rect)
                if [row, column] == self.saper.cords:
                    self.screen.blit(self.saper.img, rect)
        pygame.display.flip()

    def run(self):
        self.initialize_pygame()
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
            self.draw_grid()
            self.clock.tick(20)
        pygame.quit()


class Saper(object):

    def __init__(self, grid_quan):
        self.grid_quan = grid_quan
        self.img = pygame.image.load('board/saper.png')
        self.cords = [grid_quan-1, grid_quan-1]

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
