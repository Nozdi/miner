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
        self.create_grid()
        self.title = "Miner"
        self.done = False

    def size_by_name(self, name):
        return self.quantity * (CELL[name] + CELL['margin']) + CELL['margin']

    def create_grid(self):
        self.grid = []
        for row in xrange(self.quantity):
            self.grid.append([])
            for column in xrange(self.quantity):
                self.grid[row].append(0)

    def initialize_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()

    def draw_grid(self):
        self.screen.fill(BLACK)
        for row in xrange(self.quantity):
            for column in xrange(self.quantity):
                pygame.draw.rect(self.screen, WHITE,
                                 [(CELL['margin'] + CELL['width']) * column + CELL['margin'],
                                  (CELL['margin'] + CELL['height']) * row + CELL['margin'],
                                  CELL['width'], CELL['height']])
        pygame.display.flip()

    def run(self):
        self.initialize_pygame()
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
            self.draw_grid()
            self.clock.tick(20)
        pygame.quit()
