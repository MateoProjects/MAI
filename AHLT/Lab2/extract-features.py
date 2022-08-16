#! /usr/bin/python3

import sys
import re
from os import listdir

from xml.dom.minidom import parse
from nltk.tokenize import word_tokenize


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
our_resources.update(read_our_resources("../data/resources/drug_n.txt", 0.8, "drug_n"))
our_resources.update(read_our_resources("../data/resources/brand.txt", 0.8, "brand"))
our_resources.update(read_our_resources("../data/resources/group.txt", 0.8, "group"))


## --------- tokenize sentence ----------- 
## -- Tokenize sentence, returning tokens and span offsets

def tokenize(txt):
    offset = 0
    tks = []
    ## word_tokenize splits words, taking into account punctuations, numbers, etc.
    for t in word_tokenize(txt):
        ## keep track of the position where each token should appear, and
        ## store that information with the token
        offset = txt.find(t, offset)
        tks.append((t, offset, offset + len(t) - 1))
        offset += len(t)

    ## tks is a list of triples (word,start,end)
    return tks


## --------- get tag ----------- 
##  Find out whether given token is marked as part of an entity in the XML

def get_tag(token, spans):
    (form, start, end) = token
    for (spanS, spanE, spanT) in spans:
        if start == spanS and end <= spanE:
            return "B-" + spanT
        elif start >= spanS and end <= spanE:
            return "I-" + spanT

    return "O"


## --------- Feature extractor ----------- 
## -- Extract features for each token in given sentence

def features_from_token(token, prefix="", use_form=True, use_capitals=True,
                        use_non_chars=True, use_suf_and_pref=True, use_resources=True):
    features = []

    # Form
    if use_form:
        features.append(f"form={token}")
        features.append(f"formLC={token.lower()}")
        features.append(f"form_length={len(token)}")

    # Capitals
    if use_capitals:
        num_capitals = len(re.findall(r'[A-Z]', token))
        features.append(f"num_capitals={num_capitals}")
        if token.islower():
            features.append("is_lower")
        elif token.isupper():
            features.append("is_upper")
        elif token.istitle():
            features.append("is_title")

    # Non-characters
    if use_non_chars:
        if bool(re.search(r'\d', token)):
            features.append("has_digits")
        if bool(re.search(r'-', token)):
            features.append("has_minus")
        if bool(re.search(r'\.', token)):
            features.append("has_points")
        if bool(re.search(r'\(|\)', token)):
            features.append("has_parenthesis")
        if bool(re.search(r'\[|\]', token)):
            features.append("has_brackets")
        if bool(re.search(r'\{|\}', token)):
            features.append("has_braces")

    # Suffixes and prefixes
    if use_suf_and_pref:
        features.append(f"suf3={token[-3:]}")
        features.append(f"suf5={token[-5:]}")
        features.append(f"pref3={token[:3]}")
        features.append(f"pref5={token[:5]}")

    # External resources (not used)
    """if use_resources:
        if token in our_resources:
            features.append(f"{our_resources[token]}_in_our_resources")
        if token in external:
            features.append(f"{external[token]}_in_external_resources")"""

    # Add prefix (if required)
    if prefix != "":
        features = [prefix + feature for feature in features]

    return features


def extract_features(tokens):
    # for each token, generate list of features and add it to the result
    result = []
    for k in range(0, len(tokens)):
        tokenFeatures = []
        token = tokens[k][0]

        # Current token
        tokenFeatures += features_from_token(token)

        # Previous token
        if k > 0:
            prev_token = tokens[k - 1][0]
            tokenFeatures += features_from_token(prev_token, prefix="prev")
        else:
            tokenFeatures.append("BoS")

        # Next token
        if k < len(tokens) - 1:
            next_token = tokens[k + 1][0]
            tokenFeatures += features_from_token(next_token, prefix="next")
        else:
            tokenFeatures.append("EoS")

        result.append(tokenFeatures)

    return result


## --------- MAIN PROGRAM ----------- 
## --
## -- Usage:  baseline-NER.py target-dir
## --
## -- Extracts Drug NE from all XML files in target-dir, and writes
## -- them in the output format requested by the evalution programs.
## --


# directory with files to process
datadir = sys.argv[1]

# process each file in directory
for f in listdir(datadir):

    # parse XML file, obtaining a DOM tree
    tree = parse(datadir + "/" + f)

    # process each sentence in the file
    sentences = tree.getElementsByTagName("sentence")
    for s in sentences:
        sid = s.attributes["id"].value  # get sentence id
        spans = []
        stext = s.attributes["text"].value  # get sentence text
        entities = s.getElementsByTagName("entity")
        for e in entities:
            # for discontinuous entities, we only get the first span
            # (will not work, but there are few of them)
            (start, end) = e.attributes["charOffset"].value.split(";")[0].split("-")
            typ = e.attributes["type"].value
            spans.append((int(start), int(end), typ))

        # convert the sentence to a list of tokens
        tokens = tokenize(stext)
        # extract sentence features
        features = extract_features(tokens)

        # print features in format expected by crfsuite trainer
        for i in range(0, len(tokens)):
            # see if the token is part of an entity
            tag = get_tag(tokens[i], spans)
            print(sid, tokens[i][0], tokens[i][1], tokens[i][2], tag, "\t".join(features[i]), sep='\t')

        # blank line to separate sentences
        print()
