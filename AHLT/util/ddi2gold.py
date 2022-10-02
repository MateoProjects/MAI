#! /usr/bin/python3

# Dumps all ground truth drug-drug-interactions in given directory
# in the format expected by the evaluator.

# May be useful to compare with your output or to perform data exploration

# usage:  ./ddi2gold.py data-directory

import sys
from os import listdir
from xml.dom.minidom import parse

# directory with files to process
datadir = sys.argv[1]

# process each file in directory
for f in listdir(datadir) :
    
    tree = parse(datadir+"/"+f)

    pairs = tree.getElementsByTagName("pair")
    for p in pairs :
        if (p.attributes["ddi"].value=="true") :
            print(p.attributes["e1"].value,
                  p.attributes["e2"].value,
                  p.attributes["type"].value,
                  sep="|")
        
