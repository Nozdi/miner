from learn import learn_machine
from time import sleep


class Bot(object):
    def __init__(self, saper, display):
        self.saper = saper
        self.display = display

    def move(self, method):
        method()
        sleep(0.3)

    def run(self):
        for i in range(self.saper.grid_quan):
            yield self.move(self.saper.left)
