#! /usr/bin/python3

# Dumps all ground truth entities in given directory in the format
# expected by the evaluator.

# May be useful to compare with your output or to perform data exploration

# usage:  ./ner2gold.py data-directory

import sys
from os import listdir
from xml.dom.minidom import parse

# directory with files to process
datadir = sys.argv[1]

# process each file in directory
for f in listdir(datadir) :
    
    tree = parse(datadir+"/"+f)
    
    entities = tree.getElementsByTagName("entity")
    for e in entities :
        sent_id = ".".join(e.attributes["id"].value.split(".")[:-1])
        print(sent_id,
              e.attributes["charOffset"].value,
              e.attributes["text"].value,
              e.attributes["type"].value,
              sep="|")
        
