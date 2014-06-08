#!/usr/bin/env python

from board.display import Display
from board.decisiontree import DecisionTree
from threading import Thread

if __name__ == '__main__':
    disp = Display(20)  # 28
    thread = Thread(target=disp.run)
    thread.start()
    dec_tree = DecisionTree(disp)
