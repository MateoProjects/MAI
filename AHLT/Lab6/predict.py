#! /usr/bin/python3

import sys
from os import system

from tensorflow.keras.models import Model,load_model

from dataset import *
from codemaps import *
import evaluator

## --------- Entity extractor ----------- 
## -- Extract drug entities from given text and return them as
## -- a list of dictionaries with keys "offset", "text", and "type"

def output_interactions(data, preds, outfile) :

   #print(testdata[0])
   outf = open(outfile, 'w')
   for exmp,tag in zip(data.sentences(),preds) :
      sid = exmp['sid']
      e1 = exmp['e1']
      e2 = exmp['e2']
      if tag!='null' :
         print(sid, e1, e2, tag, sep="|", file=outf)
            
   outf.close()

   
## --------- MAIN PROGRAM ----------- 
## --
## -- Usage:  baseline-NER.py target-dir
## --
## -- Extracts Drug NE from all XML files in target-dir
## --
fname = sys.argv[1]
datafile = sys.argv[2]
outfile = sys.argv[3]

model = load_model(fname)
codes = Codemaps(fname)

testdata = Dataset(datafile)
X = codes.encode_words(testdata)

Y = model.predict(X)
Y = [codes.idx2label(np.argmax(s)) for s in Y]

# extract relations
output_interactions(testdata, Y, outfile)