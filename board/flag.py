import pygame

class Flag(object):

	def __init__(self, cords):
		self.cords = cords


class RedFlag(Flag):

	def __init__(self, cords):
		super(RedFlag, self).__init__(cords)
		self.img = pygame.image.load('board/redflag.png')


class YellowFlag(Flag):

	def __init__(self, cords):
		super(YellowFlag, self).__init__(cords)
		self.img = pygame.image.load('board/yellowflag.png')


class GreenFlag(Flag):

	def __init__(self, cords):
		super(GreenFlag, self).__init__(cords)
		self.img = pygame.image.load('board/greenflag.png')
