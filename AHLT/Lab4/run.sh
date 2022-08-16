#! /bin/bash

BASEDIR=..
export PYTHONPATH=$BASEDIR/util

$BASEDIR/util/corenlp-server.sh -quiet true -port 9000 -timeout 15000  &
sleep 1

# extract features
echo "Extracting features"
python3 extract-features.py $BASEDIR/data/devel/ > devel.cod &
python3 extract-features.py $BASEDIR/data/test/ > test.cod &
python3 extract-features.py $BASEDIR/data/train/ | cut -f4- > train.cod

kill `cat /tmp/corenlp-server.running`

# train model
echo "Training model"
./megam-64.opt -nc -nobias -repeat 6 multiclass train.cod > model.mem
# run model
echo "Running model..."
python3 predict-mem.py model.mem < devel.cod > devel.out
python3 predict-mem.py model.mem < test.cod > test.out
# evaluate results
echo "Evaluating results..."
python3 $BASEDIR/util/evaluator.py DDI $BASEDIR/data/devel/ devel.out > devel.stats
python3 $BASEDIR/util/evaluator.py DDI $BASEDIR/data/test/ test.out > test.stats

