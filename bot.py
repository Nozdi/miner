from learn import learn_machine
from time import sleep

def bot(saper):
    for i in range(saper.grid_quan):
        saper.left()
        sleep(0.1)
        yield
