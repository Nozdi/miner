import pickle
import random
import time

from board.settings import YELLOW, RED, GREEN


class NeuralNetwork(object):

    def __init__(self, disp):
        self.with_body = 0
        self.with_flag = 0
        self.net = pickle.load(open('net.pkl'))

        self.display = disp
        self.saper = self.display.saper
        self.last_move_from = 'left'
        self.visited = set()
        self.visited.add(tuple(self.saper.cords))
        self.mover = {
            'left': lambda x,y: (x, y-1),
            'right': lambda x,y: (x, y+1),
            'up': lambda x,y: (x-1, y),
            'down': lambda x,y: (x+1, y),
        }
        self.opposite = {
            'left': 'right',
            'right': 'left',
            'up': 'down',
            'down': 'up',
        }
        self.last_health = self.saper.health
        self.demining()

    def health_check(self):
        if self.last_health > self.saper.health:
            self.last_health = self.saper.health
            self.with_body += 1
            print "demined with BODY:", self.with_body
            return True
        return False

    def demining(self):
        sleep = .1
        detonated = False
        allow_flag = True
        while self.display.no_of_mines != 0:
            time.sleep(sleep)

            if self.health_check():
                getattr(self.saper, self.opposite[self.last_move_from])()
                time.sleep(sleep)

                to_move = random.choice(
                    filter(
                        lambda x: x not in [self.opposite[self.last_move_from], self.last_move_from],
                        self.mover.keys())
                )

                getattr(self.saper, to_move)()
                allow_flag = False
                continue

            color = self.nearest_mine()
            if not color:
                self.make_random_move()
                continue

            if color != self.saper.current_flag_colour and detonated:
                getattr(self.saper, self.opposite[self.last_move_from])()
                self.last_move_from = self.opposite[self.last_move_from]
                detonated = False

            self.saper.current_flag_colour = color
            if round(self.net.activate([self.display.radiations[color]]), 3) == 1:

                if not allow_flag:
                    allow_flag = True
                    continue

                getattr(self.saper, 'place_flag_' + self.last_move_from)()
                time.sleep(sleep)
                diff = self.saper.detonate()
                self.display.no_of_mines -= diff
                self.with_flag += diff
                print "demined with FLAG:", self.with_flag
                detonated = True

            self.make_random_move()

        print "with flag:", self.with_flag
        print "with body:", self.with_body

    def make_random_move(self):
        counter = 0
        append = True
        move = random.choice(self.mover.keys())

        while self.mover[move](*self.saper.cords) in self.visited:
            if counter > 18:
                append = False
                break
            move = random.choice(self.mover.keys())
            counter += 1

        if append:
            self.visited.add(self.mover[move](*self.saper.cords))

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
