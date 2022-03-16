##
## Estimates (via MLE) the parameters of a character 
## trigram model using the given corpus as training data.
##
## Usage:  python3 format-data.py <corpus.txt >features.dat

import sys
from MLEmodel import *

## ---------------------------------
def ngrams(f,n) :
  ng = "._"
  ch = f.read(1).lower()
  if ch.isspace() : ch = '_'
  ng += ch
  while ch :
    yield ng
    ch = f.read(1).lower()
    if ch.isspace() : ch = '_'
    ng = (ng+ch)[1:]

    
## MAIN ---------------------


## -- read text in ngrams, and count occurrences into a MLE model
mle = MLEmodel()

for t in ngrams(sys.stdin, 3) :
  mle.add_trigram_count(t,1)

mle.dump()
