#! /bin/bash

BASEDIR=..
export PYTHONPATH=$BASEDIR/util

# Start CoreNLP server, waiting a bit for it to start
$BASEDIR/util/corenlp-server.sh -quiet true -port 9000 -timeout 15000  &
sleep 1

# Execute the algorithm
echo "Executing the algorithm..."
python3 baseline-DDI.py $BASEDIR/data/devel devel.out > devel.stats
python3 baseline-DDI.py $BASEDIR/data/test test.out > test.stats
#python3 explore.py $BASEDIR/data/train explore.out > explore.stats
echo "Algorithm executed"

# Stop CoreNLP server
kill `cat /tmp/corenlp-server.running`
sleep 1
