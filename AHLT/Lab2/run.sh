BASEDIR=..

# Download dependencies
echo "Checking dependencies..."
pip3 install -r requirements.txt && python -c "import nltk; nltk.download('punkt')"
if [ $? -eq 0 ]; then
  echo "Dependencies installed"
else
  echo "ERROR during dependencies installation, exiting..."
  exit 1
fi

# Create directories for results (if don't exist)
features_dir="features"
mkdir -p $features_dir
models_dir="models"
mkdir -p $models_dir
results_dir="results"
mkdir -p $results_dir

# Convert datasets to feature vectors
echo "Extracting features..."
python3 extract-features.py $BASEDIR/data/train/ > $features_dir/train.feat
python3 extract-features.py $BASEDIR/data/devel/ > $features_dir/devel.feat
python3 extract-features.py $BASEDIR/data/test/ > $features_dir/test.feat

# Train CRF model
echo "Training CRF model..."
python3 train-crf.py $models_dir/model.crf < $features_dir/train.feat
# Run CRF model
echo "Running CRF model..."
python3 predict.py $models_dir/model.crf < $features_dir/devel.feat > $results_dir/devel-CRF.out
python3 predict.py $models_dir/model.crf < $features_dir/test.feat > $results_dir/test-CRF.out
# Evaluate CRF results
echo "Evaluating CRF results..."
python3 $BASEDIR/util/evaluator.py NER $BASEDIR/data/devel $results_dir/devel-CRF.out > $results_dir/devel-CRF.stats
python3 $BASEDIR/util/evaluator.py NER $BASEDIR/data/test $results_dir/test-CRF.out > $results_dir/test-CRF.stats


# MEM model commented (it will virtually never surpass the CRF model in this context and training is too slow)
: '
# Train MEM model
echo "Training MEM model..."
cat $features_dir/train.feat | cut -f5- | grep -v ^$ > $features_dir/train.mem.feat
./megam-64.opt -nobias -nc -repeat 4 multiclass $features_dir/train.mem.feat > $models_dir/model.mem
rm $features_dir/train.mem.feat
# Run MEM model
echo "Running MEM model..."
python3 predict.py $models_dir/model.mem < $features_dir/devel.feat > $results_dir/devel-MEM.out
python3 predict.py $models_dir/model.mem < $features_dir/test.feat > $results_dir/test-MEM.out
# Evaluate MEM results
echo "Evaluating MEM results..."
python3 $BASEDIR/util/evaluator.py NER $BASEDIR/data/devel $results_dir/devel-MEM.out > $results_dir/devel-MEM.stats
python3 $BASEDIR/util/evaluator.py NER $BASEDIR/data/test $results_dir/test-MEM.out > $results_dir/test-MEM.stats
'