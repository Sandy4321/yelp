
from sys import argv
import pickle
from glob import glob

from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.shortcuts import buildNetwork
from numpy import matrix

def train_model(features, target):
    rows, cols = features.shape
    train_ds = SupervisedDataSet(cols, 1)
    train_ds.setField('input', features)
    train_ds.setField('target', matrix([target]).T)

    network = buildNetwork(cols, cols / 2, 1)
    #trainer = RPropMinusTrainer(self.network, dataset=train_ds, verbose=True)
    trainer = BackpropTrainer(network, dataset=train_ds, momentum=0.1, verbose=True, weightdecay=0.01)
    trainer.trainUntilConvergence(maxEpochs=10)

def train_models(features_dir, target_dir, model_dir):
    for i, (features_file, target_file) in enumerate(zip(glob(features_dir + '/*.dat'), glob(target_dir + '/*.dat'))):
        features = pickle.load(file(features_file))
        target = pickle.load(file(target_file))
        model = train_model(features, target)
    
        pickle.dump(model, file('%s/model%s.dat' % (model_dir, i), 'w'))

if __name__ == '__main__':
    train_models(*argv[1:])
