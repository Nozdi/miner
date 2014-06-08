from time import sleep
from glob import glob
from os import path
from copy import deepcopy
from algorithms import SymbolicLearningSystem
from board.settings import RED, YELLOW, GREEN

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
            'right': self.saper.down,
            'down': self.saper.down,
        }
        self.revese_moves = {
            'up': self.saper.down,
            'left': self.saper.right,
            'right': self.saper.left,
            'down': self.saper.up,
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
            where[key] = [self.moves[move['move']] for move in where[key]]

        where = self.machine['where_place']
        for key in where:
            where[key] = [self.flag_moves[move['move']] for move in where[key]]

        place = self.machine['place']
        for key in place:
            before = place.pop(key)
            new_key = self.colors.get(key, 'all')
            place[new_key] = before['percent']

    def move(self, method):
        method()
        sleep(0.3)

    def run(self):
        last_move = 'left'

        # check if saper should put a flag
        place_flags = False
        if any([self.machine['place'] > val
                for val in self.display.radiations.values()]):
            place_flags = True

        # putting flags
        last_flag = 'none'
        if place_flags:
            for i in range(len(self.colors_priority)):
                last_flag = self.machine['flag_color'][last_flag]()
                if (self.display.radiations[last_flag] * 100 >
                   self.machine['place'][last_flag]):
                    for place in self.machine['where_place'][last_move]:
                        yield self.move(place)

                # detonation
                mines = self.saper.detonate()
                self.score += mines
                self.display.no_of_mines -= mines
                self.move(self.display.compute_mines)
                yield

        for i in range(self.saper.grid_quan):
            yield self.move(self.saper.left)
