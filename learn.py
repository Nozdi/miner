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
