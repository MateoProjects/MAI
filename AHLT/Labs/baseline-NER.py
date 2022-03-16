#! /usr/bin/python3

import sys
from os import listdir,system
import re

from xml.dom.minidom import parse
from nltk.tokenize import word_tokenize

import evaluator

## dictionary containig information from external knowledge resources
## WARNING: You may need to adjust the path to the resource files
external = {}
with open("resources/HSDB.txt") as h :
    for x in h.readlines() :
        external[x.strip().lower()] = "drug"
with open("resources/DrugBank.txt") as h :
    for x in h.readlines() :
        (n,t) = x.strip().lower().split("|")
        external[n] = t

        
## --------- tokenize sentence ----------- 
## -- Tokenize sentence, returning tokens and span offsets

def tokenize(txt):
    offset = 0
    tks = []
    for t in word_tokenize(txt):
        offset = txt.find(t, offset)
        tks.append((t, offset, offset+len(t)-1))
        offset += len(t)
    return tks

## -----------------------------------------------
## -- check if a token is a drug part, and of which type

suffixes = ['azole', 'idine', 'amine', 'mycin']

def classify_token(txt):

   # WARNING: This function must be extended with 
   #          more and better rules

   if txt.lower() in external : return external[txt.lower()]
   elif txt.isupper() : return "brand"
   elif txt[-5:] in suffixes : return "drug"
   else : return "NONE"

   

## --------- Entity extractor ----------- 
## -- Extract drug entities from given text and return them as
## -- a list of dictionaries with keys "offset", "text", and "type"

def extract_entities(stext) :

    # WARNING: This function must be extended to
    #          deal with multi-token entities.
    
    # tokenize text
    tokens = tokenize(stext)
         
    result = []
    # classify each token and decide whether it is an entity.
    for (token_txt, token_start, token_end)  in tokens:
        drug_type = classify_token(token_txt)
        
        if drug_type != "NONE" :
            e = { "offset" : str(token_start)+"-"+str(token_end),
                  "text" : stext[token_start:token_end+1],
                  "type" : drug_type
                 }
            result.append(e)
                    
    return result
      
## --------- main function ----------- 

def nerc(datadir, outfile) :
   
    # open file to write results
    outf = open(outfile, 'w')

    # process each file in input directory
    for f in listdir(datadir) :
      
        # parse XML file, obtaining a DOM tree
        tree = parse(datadir+"/"+f)
      
        # process each sentence in the file
        sentences = tree.getElementsByTagName("sentence")
        for s in sentences :
            sid = s.attributes["id"].value   # get sentence id
            stext = s.attributes["text"].value   # get sentence text
            
            # extract entities in text
            entities = extract_entities(stext)
         
            # print sentence entities in format requested for evaluation
            for e in entities :
                print(sid,
                      e["offset"],
                      e["text"],
                      e["type"],
                      sep = "|",
                      file=outf)
            
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

nerc(datadir,outfile)

evaluator.evaluate("NER", datadir, outfile)





















