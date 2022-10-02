#! /bin/bash

BASEDIR=..
export PYTHONPATH=$BASEDIR/util

# train NN
echo "Training NN"
python3 train.py $BASEDIR/data/train $BASEDIR/data/devel mymodel $BASEDIR/data/resources/DrugBank.txt

# run model on devel and test data and compute performance
echo "Predicting and evaluating"
python3 predict.py mymodel $BASEDIR/data/devel devel.out $BASEDIR/data/resources/DrugBank.txt | tee devel.stats
python3 predict.py mymodel $BASEDIR/data/test test.out $BASEDIR/data/resources/DrugBank.txt | tee test.stats
