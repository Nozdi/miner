from time import sleep
from glob import glob
from os import path
from algorithms import SymbolicLearningSystem

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
            learned[system][base] = sls.learn()[0]
    return learned


class Bot(object):
    def __init__(self, saper, display):
        self.saper = saper
        self.display = display
        self.machine = learn_machine()

    def move(self, method):
        method()
        sleep(0.3)

    def run(self):
        for i in range(self.saper.grid_quan):
            yield self.move(self.saper.left)
