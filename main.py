#!/usr/bin/env python
from board.display import Display
from board.neuralnetwork import NeuralNetwork
from threading import Thread

if __name__ == '__main__':
    disp = Display(11, "Neu")  # 28
    thread = Thread(target=disp.run)
    thread.start()
    NeuralNetwork(disp)
