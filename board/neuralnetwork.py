import pickle
import random
import time

from board.settings import YELLOW, RED, GREEN


class NeuralNetwork(object):

    def __init__(self, disp):
        self.net = pickle.load(open('net.pkl'))
        self.display = disp
        self.saper = self.display.saper
        self.last_move_from = 'left'
        self.visited = []
        self.visited.append(self.saper.cords)
        self.demining()

    def demining(self):
        while self.display.no_of_mines != 0:
            time.sleep(.1)
            color = self.nearest_mine()
            if not color:
                self.make_random_move()
                continue

            self.saper.current_flag_colour = color
            if round(self.net.activate([self.display.radiations[color]]), 3) == 1:
                getattr(self.saper, 'place_flag_' + self.last_move_from)()
                time.sleep(.1)
                self.saper.detonate()

            self.make_random_move()


    def make_random_move(self):
        mover = {
            'left', 'right', 'up', 'down'
        }
        move = random.choice(['left', 'right', 'up', 'down'])
        if self.
        getattr(self.saper, move)()
        self.last_move_from = move


    def nearest_mine(self):
        nearest = self.net.activate([0])  # the biggest posible value
        ret = None
        for color in self.display.radiations:
            value = self.net.activate([self.display.radiations[color]])

            if value < nearest:
                nearest = value
                ret = color

        return ret
