from time import sleep
from glob import glob
from os import path
from copy import deepcopy
from algorithms import SymbolicLearningSystem
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

    def run(self):
        last_move = 'left'
        last_percents = {
            RED: 0,
            YELLOW: 0,
            GREEN: 0,
        }
        mines = 0
        while self.display.no_of_mines > 0 and self.saper.no_of_flags > 0:
            place_flags = False

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
                                    self.palces_detonated.append(coords_to_put)

            # if there was a mine think one more time!
            if mines:
                mines = 0
                continue

            #percents growing
            if any([self.display.radiations[key] > last_percents[key]
                    for key in last_percents]):
                key = random.choice(self.machine['where'][last_move].keys())
                self.move(self.machine['where'][last_move][key])
                print("Poprzedni: {} i rosnie wiec ide {}".format(last_move, key))
                last_move = key
                yield
            #all percents falling
            elif all([self.display.radiations[key] < last_percents[key]
                      for key in last_percents]):
                print("Cofam")
                key = self.revese_moves[last_move]
                self.move(self.moves[key])
                last_move = key
                yield
            # constant situation - we don't know where we should go
            else:
                print("Random ruch")
                key = random.choice(self.moves.keys())
                self.move(self.moves[key])
                last_move = key
                yield
