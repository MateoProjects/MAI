#! /usr/bin/python3
## -------------------- Imports ---------------------- ##
import sys
from os import listdir, system
import re

from xml.dom.minidom import parse
from nltk.tokenize import word_tokenize

sys.path.insert(1, "../util")
import evaluator


## -------------------- External resources ---------------------- ##
## dictionary containig information from external knowledge resources
## WARNING: You may need to adjust the path to the resource files
external = {}
with open("../data/resources/HSDB.txt") as h:
    for x in h.readlines() :
        external[x.strip().lower()] = "drug"
with open("../data/resources/DrugBank.txt") as h:
    for x in h.readlines():
        (n,t) = x.strip().lower().split("|")
        external[n] = t


## -------------------- Our resources ---------------------- ##
# This files contain the words for each specific class found in training,
# sorted by number of instances (ascendent).
# Each line contains "[count] [word]", where [count] is the number of instances.
# We consider the most frequent words using the acceptance_threshold.
# The lower the acceptance_threshold (down to 0), the more infrequent words are considered.
# Oppositely, if the acceptance_threshold is high (up to 1), only frequent words are considered.
# Also, high acceptance_threshold usually means less recall but more precision.
# One acceptance_threshold per class is defined.
def read_our_resources(filename, acceptance_threshold, type):
    res_dict = {}
    with open(filename) as f:
        elems = [x.strip().lower().split()[1] for x in f.readlines()]
        elems = elems[int(len(elems)*acceptance_threshold):]
        res_dict = { elem : type for elem in elems }
    return res_dict

our_resources = {}
our_resources.update(read_our_resources("../data/resources/drug.txt", 0.8, "drug"))
our_resources.update(read_our_resources("../data/resources/drug_n.txt", 0.5, "drug_n"))
our_resources.update(read_our_resources("../data/resources/brand.txt", 0, "brand"))
our_resources.update(read_our_resources("../data/resources/group.txt", 0, "group"))


## -------------------- Classify token ---------------------- ##
## -- check if a token is a drug part, and of which type
def classify_token(txt):
    txt_lower = txt.lower()

    if txt_lower in our_resources: return our_resources[txt_lower]
    elif txt_lower in external: return external[txt_lower]
    else: return "NONE"


## -------------------- Tokenize sentence ---------------------- ##
## -- Tokenize sentence, returning tokens and span offsets
def tokenize(txt):
    offset = 0
    tks = []
    for t in word_tokenize(txt):
        offset = txt.find(t, offset)
        tks.append((t, offset, offset+len(t)-1))
        offset += len(t)
    return tks


## -------------------- Entity extractor -------------------- ##
## -- Extract drug entities from given text and return them as
## -- a list of dictionaries with keys "offset", "text", and "type"
## -- EXTENDED for detecting multi-token entites
def extract_entities(stext, use_multi_token=False):

    # tokenize text
    tokens = tokenize(stext)

    result = []
    # classify each token and decide whether it is an entity.
    last_drug_type = None
    last_token_start = -1
    last_token_end = -1
    in_multi_token = False
    for (token_txt, token_start, token_end)  in tokens:
        drug_type = classify_token(token_txt)

        if drug_type != "NONE":
            if not use_multi_token:
                e = { "offset" : str(token_start)+"-"+str(token_end),
                      "text" : stext[token_start:token_end+1],
                      "type" : drug_type
                     }
                result.append(e)
            # If using multi-token
            else:
                if in_multi_token:
                    if drug_type == last_drug_type:
                        last_token_end = token_end
                    else:
                        # Add the previous multi-token
                        e = { "offset" : str(last_token_start)+"-"+str(last_token_end),
                              "text" : stext[last_token_start:last_token_end+1],
                              "type" : last_drug_type
                             }
                        result.append(e)
                        # Prepare for the next multi-token
                        last_drug_type = drug_type
                        last_token_start = token_start
                        last_token_end = token_end
                else:
                    # Prepare for the next multi-token
                    last_drug_type = drug_type
                    last_token_start = token_start
                    last_token_end = token_end
                    in_multi_token = True
        elif use_multi_token:
            if in_multi_token:
                # Multi-token stops
                in_multi_token = False
                # Add the previous multi-token
                e = { "offset" : str(last_token_start)+"-"+str(last_token_end),
                      "text" : stext[last_token_start:last_token_end+1],
                      "type" : last_drug_type
                     }
                result.append(e)

    # Add the last multi-token
    if in_multi_token:
        e = { "offset" : str(last_token_start)+"-"+str(last_token_end),
              "text" : stext[last_token_start:last_token_end+1],
              "type" : last_drug_type
             }
        result.append(e)


    return result


## -------------------- Main function -------------------- ##
def nerc(datadir, outfile, use_multi_token) :

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
            entities = extract_entities(stext, use_multi_token)

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
## -- Usage:  baseline-NER.py target-dir outfile [use_multi_token (if == "multi")]
## --
## -- Extracts Drug NE from all XML files in target-dir
## --

# directory with files to process
datadir = sys.argv[1]
outfile = sys.argv[2]

# Use multi-token argument
use_multi_token = False
if len(sys.argv) > 3:
    use_multi_token = sys.argv[3].lower() == "multi"

nerc(datadir, outfile, use_multi_token)

evaluator.evaluate("NER", datadir, outfile)
