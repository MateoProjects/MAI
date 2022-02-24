##
## Loads a MLE trigram model, and uses it to generate
## sequences of given length.
##
##  Usage:   python3 generate.py model.dat length
##

import sys
import random

from MLEmodel import *
    
## ---------------------------------
## Given a bigram xy, randomly select z, according to distribution
def transition(xy) :
  global model

  # get distribution of possible z after xy
  dist = model.prob_dist_z(xy)

  # randomly select a z according to distribution
  r = random.random()
  s = 0.0
  for c in dist :
    s = s + dist[c]
    if (s>r) : return c


## MAIN ---------------------

## -- load MLE trigram model
model = MLEmodel(sys.argv[1])

## length to generate
maxc = int(sys.argv[2])

## select a random initial state "._z" using probabilities in ptr
x="."; y="_";
z=transition(x+y)
print("\n"+z, end="")

for i in range(1,maxc) :
  ## select a random next state, according to transition probabilities
  x=y; y=z; z=transition(x+y)

  ## write character for selected state.
  if (z=="_") : print(" ", end="")
  else : print(z, end="")

print("")
