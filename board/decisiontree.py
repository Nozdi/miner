from settings import (
    RED,
    YELLOW,
    GREEN,
)
from .mine import Scheme, RedMine, YellowMine, GreenMine
import time

class DecisionTree(object):

    def __init__(self, display):
        self.display = display
        self.saper = self.display.saper
        self.mines_schemes = {
            RED: Scheme(0, RedMine),
            YELLOW: Scheme(0, YellowMine),
            GREEN: Scheme(0, GreenMine)
        }
        self.danger_radiation = 1
        self.history = [self.mines_schemes, self.danger_radiation]
        #import ipdb; ipdb.set_trace()
        self.cost = 0
        self.decision_tree(self.history, self.cost)


    def decision_tree(self, history, cost):
        while self.saper.cords != [self.display.quantity-1, 0]:
            if self.display.radiations[RED] >= self.history[1]:
                self.saper.current_flag_colour = RedMine.color
                self.saper.place_flag_left()
                self.cost += 1
                self.saper.place_flag_up()
                self.cost += 1
                self.display.no_of_mines -= self.saper.detonate()
                self.cost += 1
            if self.display.radiations[YELLOW] >= self.history[1]:
                self.saper.current_flag_colour = YellowMine.color
                self.saper.place_flag_left()
                self.cost += 1
                self.saper.place_flag_up()
                self.cost += 1
                self.display.no_of_mines -= self.saper.detonate()
                self.cost += 1
            if self.display.radiations[GREEN] >= self.history[1]:
                self.saper.current_flag_colour = GreenMine.color
                self.saper.place_flag_left()
                self.cost += 1
                self.saper.place_flag_up()
                self.cost += 1
                self.display.no_of_mines -= self.saper.detonate()
                self.cost += 1
                self.saper.left()
                self.cost += 1
            else:
                self.saper.left()
                self.cost += 1
                print self.cost
            time.sleep(0.4)