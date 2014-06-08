import pygame
from settings import RED, YELLOW, GREEN


class Flag(object):

    def __init__(self, coords):
        self.coords = coords


class RedFlag(Flag):
    colour = RED

    def __init__(self, coords):
        super(RedFlag, self).__init__(coords)
        self.img = pygame.image.load('board/redflag.png')


class YellowFlag(Flag):
    colour = YELLOW

    def __init__(self, coords):
        super(YellowFlag, self).__init__(coords)
        self.img = pygame.image.load('board/yellowflag.png')


class GreenFlag(Flag):
    colour = GREEN

    def __init__(self, coords):
        super(GreenFlag, self).__init__(coords)
        self.img = pygame.image.load('board/greenflag.png')
