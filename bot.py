from time import sleep
from glob import glob
from os import path
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
            'down': self.saper.down,
            'left': self.saper.left,
            'right': self.saper.down,
        }
        self.revese_moves = {
            'up': self.saper.down,
            'left': self.saper.right,
            'right': self.saper.left,
            'down': self.saper.up,
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
        self.machine_to_functions()

    def machine_to_functions(self):
        flag_color = self.machine['flag_color']
        for key in flag_color:
            flag_color[key] = self.flag[flag_color[key]['place_flag']]

        where = self.machine['where']
        for key in where:
            where[key] = [self.moves[move['move']] for move in where[key]]

        place = self.machine['place']
        for key in place:
            before = place.pop(key)
            new_key = self.colors.get(key, 'all')
            place[new_key] = before['percent']

    def move(self, method):
        method()
        sleep(0.3)

    def run(self):
        print(self.display.radiations)

        for i in range(self.saper.grid_quan):
            yield self.move(self.saper.left)
