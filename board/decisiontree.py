from settings import (
    RED,
    YELLOW,
    GREEN,
)
from .mine import Scheme, RedMine, YellowMine, GreenMine
import time
import random

class DecisionTree(object):

    def __init__(self, display):
        self.display = display
        self.saper = self.display.saper
        self.mines_schemes = {
            RED: Scheme(0, RedMine),
            YELLOW: Scheme(0, YellowMine),
            GREEN: Scheme(0, GreenMine)
        }
        self.danger_radiation = 0.99
        self.previous_radiation = {
            RED: 0,
            YELLOW: 0,
            GREEN: 0
        }
        self.prev_no_of_mines = self.display.no_of_mines
        #self.history = [self.mines_schemes, self.danger_radiation]
        self.history = [self.previous_radiation, self.danger_radiation, self.prev_no_of_mines]
        #import ipdb; ipdb.set_trace()
        self.cost = 0
        self.decision_tree(self.history, self.cost)

    def rand_step(self, no):
        if no == 0:
            self.saper.up()
        elif no == 1:
            self.saper.down()
        elif no == 2:
            self.saper.left()
        else:
            self.saper.right()

    def tree(self,color, history):
        self.color = color
        self.history = history

        count = 1
        no = 0
        sth = 0

        self.change = 0
        if self.display.radiations[self.color] >= self.history[1]:
            while self.display.radiations[self.color] >= self.history[1] and no < 1:
                #self.history[0][RED] = self.display.radiations[RED]
                self.saper.current_flag_colour = self.color
                self.change = 0
                while self.change == 0:
                    self.saper.place_flag_left()
                    time.sleep(count)
                    self.display.no_of_mines -= self.saper.detonate()
                    self.display.compute_mines()
                    if self.display.no_of_mines == self.history[2]:
                        self.change = 1
                    else:
                        self.history[2] = self.display.no_of_mines
                        self.saper.left()
                        time.sleep(count)
                        self.change = 0
                        sth = 1
                        break
                    self.saper.place_flag_up()
                    time.sleep(count)
                    self.display.no_of_mines -= self.saper.detonate()
                    self.display.compute_mines()
                    if self.display.no_of_mines == self.history[2]:
                        self.change = 1
                    else:
                        self.saper.up()
                        self.history[2] = self.display.no_of_mines
                        time.sleep(count)
                        self.change = 0
                        sth = 1
                        break
                    self.saper.place_flag_down()
                    time.sleep(count)
                    self.display.no_of_mines -= self.saper.detonate()
                    self.display.compute_mines()
                    if self.display.no_of_mines == self.history[2]:
                        self.change = 1
                    else:
                        self.saper.down()
                        self.history[2] = self.display.no_of_mines
                        time.sleep(count)
                        self.change = 0
                        sth = 1
                        break
                    self.saper.place_flag_right()
                    time.sleep(count)
                    self.display.no_of_mines -= self.saper.detonate()
                    self.display.compute_mines()
                    if self.display.no_of_mines == self.history[2]:
                        self.change = 1
                    else:
                        self.saper.right()
                        self.history[2] = self.display.no_of_mines
                        time.sleep(count)
                        self.change = 0
                        sth = 1
                        break
                    if self.change == 1:
                        no += 1
                        break
        if sth == 1:
            pass
        else:
            sth = 2
        return sth

    def decision_tree(self, history, cost):
        self.history = history

        count = 0.5

        while self.display.no_of_mines != 0:

            k = self.tree(RED, self.history)
            if k == 1:
                pass
            else:
                pass

            b = 1
            while b == 1:
                a = self.tree(YELLOW, self.history)
                if a == 1:
                    c = self.tree(RED, self.history)
                    if c == 1:
                        b = 0
                        break
                    else:
                        d = self.tree(GREEN, self.history)
                        if d == 1:
                            e = self.tree(RED, self,history)
                            if e == 1:
                                b = 0
                                break
                            else:
                                b = 0
                                break
                        else:
                            b = 0
                            break
                else:
                    f = self.tree(GREEN, self.history)
                    if f == 1:
                        g = self.tree(RED, self.history)
                        if g == 1:
                            b = 0
                            break
                        else:
                            h = self.tree(GREEN, self.history)
                            if h == 1:
                                i = self.tree(RED, self,history)
                                if i == 1:
                                    b = 0
                                    break
                                else:
                                    b = 0
                                    break
                            else:
                                b = 0
                                break
                    else:
                        b = 0
                        break

            self.rand_step(random.randint(0,3))
            time.sleep(count)