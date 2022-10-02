#! /usr/bin/python3

import sys
from os import listdir

from xml.dom.minidom import parse

from deptree import *
from patterns import * 

## ------------------- 
## -- Generates features for a set of tokens (used at extract_features)
def tokens_features(tree, entities, start_tk, end_tk, suffix, feats):
    for tk in range(start_tk, end_tk):
        if not tree.is_stopword(tk):
            word = tree.get_word(tk)
            lemma = tree.get_lemma(tk).lower()
            tag = tree.get_tag(tk)
            #feats.add(f"l{suffix}={lemma}")
            #feats.add(f"w{suffix}={word}")
            feats.add(f"lt{suffix}={lemma}_{tag}")
            
            # Feature indicating the presence of an entity in previous to E1
            if tree.is_entity(tk, entities):
                feats.add(f"e{suffix}")

## ------------------- 
## -- Convert a pair of drugs and their context in a feature vector
def extract_features(tree, entities, e1, e2):
    feats = set()

    # get head token for each gold entity
    tkE1 = tree.get_fragment_head(entities[e1]['start'], entities[e1]['end'])
    tkE2 = tree.get_fragment_head(entities[e2]['start'], entities[e2]['end'])

    if tkE1 is not None and tkE2 is not None:

        # Least Common Subsumer (LCS)
        lcs = tree.get_LCS(tkE1, tkE2)
        lcs_lemma = tree.get_lemma(lcs)
        lcs_tag = tree.get_tag(lcs)
        feats.add("lcs_lemma_tag=" + lcs_lemma + "_" + lcs_tag)
        
        # Get info from LCS ancestors and brothers
        lcs_ancestors = tree.get_ancestors(lcs)
        for ancestor in lcs_ancestors:
            # Add ancestor
            ancestor_lemma = tree.get_lemma(ancestor)
            ancestor_tag = tree.get_tag(ancestor)
            feats.add(f"lcs_ancestor_lemma_tag={ancestor_lemma}_{ancestor_tag}")
            # Get brothers of LCS
            brothers = tree.get_children(ancestor)
            for bro in brothers:
                if bro != lcs:
                    bro_lemma = tree.get_lemma(bro)
                    bro_tag = tree.get_tag(bro)
                    feats.add(f"lcs_bro_lemma_tag={bro_lemma}_{bro_tag}")
        
        # Features for tokens previous to(PT) E1
        tokens_features(tree, entities, 0, tkE1, "pt", feats)

        # Features for tokens in between(IB) E1 and E2
        tokens_features(tree, entities, tkE1 + 1, tkE2, "ib", feats)
        
        # Features after(A) tokens E1
        tokens_features(tree, entities, tkE2+1, tree.get_n_nodes(), "a", feats)
        
        # Features about paths in the tree
        path1 = tree.get_up_path(tkE1, lcs)
        path1 = "<".join([tree.get_lemma(x) + "_" + tree.get_rel(x) for x in path1])
        feats.add("path1=" + path1)

        path2 = tree.get_down_path(lcs, tkE2)
        path2 = ">".join([tree.get_lemma(x) + "_" + tree.get_rel(x) for x in path2])
        feats.add("path2=" + path2)

        path = path1 + "<" + tree.get_lemma(lcs) + "_" + tree.get_rel(lcs) + ">" + path2
        feats.add("path=" + path)

        # Our custom path features with tag and relationship
        path1 = tree.get_up_path(tkE1, lcs)
        path1 = "<".join([tree.get_tag(x) + "_" + tree.get_rel(x) for x in path1])
        feats.add("path1_tag_rel=" + path1)

        path2 = tree.get_down_path(lcs, tkE2)
        path2 = ">".join([tree.get_tag(x) + "_" + tree.get_rel(x) for x in path2])
        feats.add("path2_tag_rel=" + path2)

        path = path1 + "<" + tree.get_tag(lcs) + "_" + tree.get_rel(lcs) + ">" + path2
        feats.add("path_tag_rel=" + path)
        
        # Rule-based patterns
        lcs_svo = check_LCS_svo(tree, tkE1, tkE2)
        if lcs_svo is not None:
            feats.add("pattern_lcs_svo=" + lcs_svo)
    
    return feats


## --------- MAIN PROGRAM ----------- 
## --
## -- Usage:  extract_features targetdir
## --
## -- Extracts feature vectors for DD interaction pairs from all XML files in target-dir
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
        stext = s.attributes["text"].value  # get sentence text
        # load sentence entities
        entities = {}
        ents = s.getElementsByTagName("entity")
        for e in ents:
            id = e.attributes["id"].value
            offs = e.attributes["charOffset"].value.split("-")
            entities[id] = {'start': int(offs[0]), 'end': int(offs[-1])}

        # there are no entity pairs, skip sentence
        if len(entities) <= 1: continue

        # analyze sentence
        analysis = deptree(stext)

        # for each pair in the sentence, decide whether it is DDI and its type
        pairs = s.getElementsByTagName("pair")
        for p in pairs:
            # ground truth
            ddi = p.attributes["ddi"].value
            if (ddi == "true"):
                dditype = p.attributes["type"].value
            else:
                dditype = "null"
            # target entities
            id_e1 = p.attributes["e1"].value
            id_e2 = p.attributes["e2"].value
            # feature extraction

            feats = extract_features(analysis, entities, id_e1, id_e2)
            # resulting vector
            print(sid, id_e1, id_e2, dditype, "\t".join(feats), sep="\t")
