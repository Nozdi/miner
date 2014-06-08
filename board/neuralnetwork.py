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
        self.visited = set()
        self.visited.add(tuple(self.saper.cords))
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
            'left': lambda x,y: (x, y-1),
            'right': lambda x,y: (x, y+1),
            'up': lambda x,y: (x-1, y),
            'down': lambda x,y: (x+1, y),
        }

        counter = 0
        append = True
        move = random.choice(mover.keys())
        while mover[move](*self.saper.cords) in self.visited:
            if counter > 8:
                append = False
                break
            move = random.choice(mover.keys())
            counter += 1

        getattr(self.saper, move)()
        if append:
            self.visited.add(tuple(self.saper.cords))
        print self.visited
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
