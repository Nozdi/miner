from __future__ import division
from time import sleep
from glob import glob
from os import path
from copy import deepcopy
from algorithms import SymbolicLearningSystem
from itertools import product
from board.settings import RED, YELLOW, GREEN
import random

BASEDIR = "./learning_sets"


def learn_machine():
    systems = [path.basename(path.normpath(full_dirname))
               for full_dirname in glob(BASEDIR + "/*")
               if path.isdir(full_dirname)]

    learned = {}
    for system in systems:
        learned[system] = {}
        for filename in glob("{}/{}/*".format(BASEDIR, system)):
            sls = SymbolicLearningSystem.from_yaml(filename)
            base = path.splitext(path.basename(path.normpath(filename)))[0]
            result = sls.learn()
            learned[system][base] = result[0] if len(result) == 1 else result
    return learned


class Bot(object):
    def __init__(self, saper, display):
        self.saper = saper
        self.display = display
        self.all_mines = self.display.no_of_mines

        self.where_was_not = list(product(
            range(self.saper.grid_quan+1),
            repeat=2
        ))
        self.all_reds = self.display.no_of_schemes * 3

        self.machine = learn_machine()
        self.moves = {
            'up': self.saper.up,
            'left': self.saper.left,
            'right': self.saper.right,
            'down': self.saper.down,
        }
        self.revese_moves = {
            'up': 'down',
            'left': 'right',
            'right': 'left',
            'down': 'up',
        }
        self.flag_moves = {
            'up': self.saper.place_flag_up,
            'left': self.saper.place_flag_left,
            'right': self.saper.place_flag_right,
            'down': self.saper.place_flag_down,
        }
        self.colors = {
            'red': RED,
            'yellow': YELLOW,
            'green': GREEN,
        }
        self.flag = {
            'red': self.saper.red_flag,
            'yellow': self.saper.yellow_flag,
            'green': self.saper.green_flag,
        }
        self.already_located = {
            RED: [],
            YELLOW: [],
            GREEN: [],
        }
        self.palces_detonated = []
        self.score = 0
        self.colors_priority = [RED, YELLOW, GREEN]
        self.machine_to_functions()

    def machine_to_functions(self):
        self.machine['where_place'] = deepcopy(self.machine['where'])

        flag_color = self.machine['flag_color']
        for key in flag_color:
            color = flag_color.pop(key)
            new_key = self.colors.get(key, 'none')
            flag_color[new_key] = self.flag[color['place_flag']]

        where = self.machine['where']
        for key in where:
            where[key] = {move['move']: self.moves[move['move']]
                          for move in where[key]}

        where = self.machine['where_place']
        for key in where:
            where[key] = {move['move']: self.flag_moves[move['move']]
                          for move in where[key]}

        percent = self.machine['percent']
        for key in percent:
            pom = percent.pop(key)
            new_key = self.colors[key]
            percent[new_key] = pom['percent']

        place = self.machine['place']
        for key in place:
            before = place.pop(key)
            new_key = self.colors.get(key, 'all')
            place[new_key] = before['percent']/100.

    def left(self):
        if self.saper.coords[1] > 0:
            return self.saper.coords[0], self.saper.coords[1] - 1

    def right(self):
        if self.saper.coords[1] < self.saper.grid_quan-1:
            return self.saper.coords[0], self.saper.coords[1] + 1

    def up(self):
        if self.saper.coords[0] > 0:
            return self.saper.coords[0] - 1, self.saper.coords[1]

    def down(self):
        if self.saper.coords[0] < self.saper.grid_quan-1:
            return self.saper.coords[0] + 1, self.saper.coords[1]

    def move(self, method):
        method()
        sleep(0.01)

    def update_last_percents(self):
        for key in self.last_percents:
            self.last_percents[key] = self.display.radiations[key]


    def run(self):
        last_move = 'left'
        self.last_percents = {
            RED: 0,
            YELLOW: 0,
            GREEN: 0,
        }
        mines = 0
        reds = 0
        while self.display.no_of_mines > 0:
            place_flags = False

            coords = tuple(self.saper.coords)
            if coords in self.where_was_not:
                self.where_was_not.remove(coords)

            # check if saper should put a flag
            if any([val > self.machine['place']['all']
                    for val in self.display.radiations.values()]):
                place_flags = True

            # putting flags
            last_flag = 'none'
            if place_flags:
                for i in range(len(self.colors_priority)):
                    last_flag = self.machine['flag_color'][last_flag]()

                    if (self.display.radiations[last_flag] >
                       self.machine['place'][last_flag]):

                        move = self.machine['where_place'][last_move]
                        flags_on_map = self.display.no_of_mines/self.all_mines * 100

                        if (last_flag in [GREEN, YELLOW]
                           and not (reds/self.all_reds>0.85)):

                            maximal = self.machine['percent'][last_flag]
                            if flags_on_map < maximal:
                                continue

                            if last_flag == GREEN:
                                move = {
                                    last_move: move[last_move]
                                }
                            elif last_flag == YELLOW:
                                move = {
                                    key: move[key]
                                    for key in random.sample(move.keys(), 2)
                                }

                        for place in move:
                            coords_to_put = getattr(self, place)()

                            if (coords_to_put and
                               coords_to_put not in self.already_located[last_flag]
                               and coords_to_put not in self.palces_detonated):

                                print("Ostatni: {} wiec flaga: {}".format(last_move, place))
                                self.already_located[last_flag].append(coords_to_put)
                                yield self.move(move[place])

                                # detonation
                                mines = self.saper.detonate()

                                self.score += mines
                                self.display.no_of_mines -= mines
                                self.move(self.display.compute_mines)
                                yield

                                # remeber what was detonated
                                if mines:
                                    self.update_last_percents()
                                    self.palces_detonated.append(coords_to_put)
                                    if last_flag == RED:
                                        reds += 1

            # if there was a mine think one more time!
            if mines:
                mines = 0
                continue

            radiations = self.display.radiations
            #percents growing
            if any([(radiations[key] > self.last_percents[key] or radiations[key] == 1.0)
                    for key in self.last_percents]):

                key = random.choice(self.machine['where'][last_move].keys())
                self.move(self.machine['where'][last_move][key])
                print("Poprzedni: {} i rosnie wiec ide {}".format(last_move, key))
                last_move = key
                self.update_last_percents()
                yield

            #all percents falling
            elif any([radiations[key] < self.last_percents[key]
                      for key in self.last_percents]):
                print("Cofam")
                key = self.revese_moves[last_move]
                self.move(self.moves[key])
                last_move = key
                self.update_last_percents()
                yield
            # constant situation - we don't know where we should go
            else:
                print("Idz gdzie nie byles")
                sx, sy = self.saper.coords
                px, py = self.where_was_not[0]
                if sy > py:
                    last_move = 'left'
                elif sy < py:
                    last_move = 'right'
                elif sx > px:
                    last_move = 'up'
                elif sx < px:
                    last_move = 'down'

                self.move(self.moves[last_move])
                self.update_last_percents()
                yield
