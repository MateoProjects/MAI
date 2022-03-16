##
## Loads a MLE trigram model, and uses it to compute
## the probabilitity of the input sequence
##
##  Usage:   python3 prob.py model.dat <text
##

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

## -- load MLE trigram model
model = MLEmodel(sys.argv[1])

## compute input probability
prob=1.0;

for xyz in ngrams(sys.stdin, 3) :
  xy = xyz[0:2]
  z = xyz[2]
  pt = model.conditional_prob(xy,z)
  prob = prob * pt
  print("{:s} {:.20g} {:.20g}".format(xyz,pt,prob))

print("\nSequence probability: {:.10g}".format(prob))
