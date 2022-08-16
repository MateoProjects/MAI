#! /usr/bin/python3

import sys
import re
from os import listdir

from xml.dom.minidom import parse
import evaluator

from deptree import *
import patterns

## ------------------- 
## -- check if a pair has an interaction and of which type, applying a cascade of rules.

def check_interaction(tree, entities, e1, e2):

   # get head token for each gold entity
   tkE1 = tree.get_fragment_head(entities[e1]['start'],entities[e1]['end'])
   tkE2 = tree.get_fragment_head(entities[e2]['start'],entities[e2]['end'])

   # Custom very specific pattern
   #p = patterns.check_LCS_VB_rels(tree,tkE1,tkE2)
   #if p is not None: return p

   # Custom specific pattern
   p = patterns.check_LCS_VB_parent(tree, tkE1, tkE2)
   if p is not None: return p

   # Pre-defined and improved pattern 1
   p = patterns.check_LCS_svo(tree,tkE1,tkE2)
   if p is not None: return p
   
   # Pre-defined and improved pattern 2
   p = patterns.check_wib(tree,tkE1,tkE2,entities,e1,e2)
   if p is not None: return p

   # Custom general pattern
   p = patterns.check_LCS_VB_NN(tree,tkE1,tkE2)
   if p is not None: return p

   return "null"


## --------- detect drug-drug interactions in given dataset ----------- 
def ddi(datadir, outfile) :

   outf = open(outfile, 'w')
   # process each file in directory
   for f in listdir(datadir) :

      # parse XML file, obtaining a DOM tree
      tree = parse(datadir+"/"+f)

      # process each sentence in the file
      sentences = tree.getElementsByTagName("sentence")
      for s in sentences:
         sid = s.attributes["id"].value   # get sentence id
         stext = s.attributes["text"].value   # get sentence text

         analysis = deptree(stext)
        
         # load sentence entities
         entities = {}
         ents = s.getElementsByTagName("entity")
         for e in ents:
            id = e.attributes["id"].value
            offs = e.attributes["charOffset"].value.split("-")           
            entities[id] = {'start': int(offs[0]), 'end': int(offs[-1])}

         # for each pair in the sentence, decide whether it is DDI and its type
         pairs = s.getElementsByTagName("pair")
         for p in pairs:
            id_e1 = p.attributes["e1"].value
            id_e2 = p.attributes["e2"].value
            ddi_type = check_interaction(analysis, entities, id_e1, id_e2)
            if ddi_type != "null":
               print("|".join([sid, id_e1, id_e2, ddi_type]), file=outf)

   outf.close()


## --------- MAIN PROGRAM ----------- 
## --
## -- Usage:  baseline-NER.py target-dir
## --
## -- Extracts Drug NE from all XML files in target-dir
## --


# directory with files to process
datadir = sys.argv[1]
outfile = sys.argv[2]

ddi(datadir,outfile)

evaluator.evaluate("DDI", datadir, outfile)

