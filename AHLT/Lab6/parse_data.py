
import sys
from dataset import *

# preprocess a dataset with StanfordCore, and store it in a pickle file for later use
# usage:  ./parse_data.py data-folder filename
#   e.g.  ./parse_data.py ../../data/train train

datadir = sys.argv[1]
filename =  sys.argv[2]

data = Dataset(datadir)
data.save(filename)
