#! /usr/bin/env python
# -*- coding: utf-8 -*-
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
import random
import pickle


dataModel = [
    [0.145, 5],
    [0.316, 3.1622776], # sqrt(10)
    [0.8298, 2],
    [1, 1],
]

ds = SupervisedDataSet(1, 1)
for inp, tar in dataModel:
    ds.addSample(inp, tar)

trainingSet = SupervisedDataSet(1, 1);
for _ in range(0,1000):
    bit = random.choice(dataModel)
    trainingSet.addSample(bit[0], bit[1])

net = buildNetwork(1, 4, 1, bias=True)

trainer = BackpropTrainer(net, ds, learningrate = 0.001, momentum = 0.99)
trainer.trainUntilConvergence(verbose=True,
                              dataset=trainingSet,
                              maxEpochs=100)

pickle.dump(net, open('net.pkl', 'w'))