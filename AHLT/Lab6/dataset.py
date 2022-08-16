
from os import listdir
from xml.dom.minidom import parse

import pickle
from deptree import *

class Dataset:
    ##  Parse all XML files in given dir, and load a list of sentences.
    ##  Each sentence is a list of tuples (word, start, end, tag)
    def __init__(self, filename) :

        if filename[-4:] == ".pck" :
            # parameter is a pickle file, load it
            with open(filename, "rb") as pf:
                self.data = pickle.load(pf)

        else :
            # parameter must be a folder with XML data, load it
            self.data = []
            
            # process each file in directory
            for f in listdir(filename) :
   
                # parse XML file, obtaining a DOM tree
                tree = parse(filename+"/"+f)
   
                # process each sentence in the file
                sentences = tree.getElementsByTagName("sentence")
                for s in sentences :
                    sid = s.attributes["id"].value   # get sentence id
                    stext = s.attributes["text"].value   # get sentence text
                    ents = s.getElementsByTagName("entity")

                    # there are no entity pairs, skip sentence
                    if len(ents) <= 1 : continue
                
                    entities = {}
                    for e in ents :
                        # for discontinuous entities, we only get the first span
                        # (will not work, but there are few of them)
                        eid =  e.attributes["id"].value
                        typ =  e.attributes["type"].value
                        (start,end) = e.attributes["charOffset"].value.split(";")[0].split("-")
                        entities[eid] = {"start":int(start), "end":int(end), "type": typ}
          
                    # analyze sentence with stanford parser.
                    tree = deptree(stext)

                    # for each pair in the sentence, get whether it is DDI and its type
                    pairs = s.getElementsByTagName("pair")
                    for p in pairs:
                        # ground truth
                        ddi = p.attributes["ddi"].value
                        if (ddi=="true") : dditype = p.attributes["type"].value
                        else : dditype = "null"
                        # target entities
                        e1 = p.attributes["e1"].value
                        e2 = p.attributes["e2"].value
                    
                        sent = []
                        seen = set([])
                        for tk in range(1,tree.get_n_nodes()) :
                            tk_start,tk_end = tree.get_offset_span(tk)
                            tk_ent = tree.is_entity(tk, entities)
                            
                            if tk_ent is None : token = {'form': tree.get_word(tk), 'lc_form':tree.get_word(tk).lower(), 'lemma': tree.get_lemma(tk), 'pos': tree.get_tag(tk)}
                            elif tk_ent == e1 : token = {'form':'<DRUG1>', 'lc_form':'<DRUG1>', 'lemma':'<DRUG1>', 'pos':'<DRUG1>', 'etype':entities[e1]['type']}
                            elif tk_ent == e2 : token = {'form':'<DRUG2>', 'lc_form':'<DRUG1>', 'lemma':'<DRUG2>', 'pos':'<DRUG2>', 'etype':entities[e2]['type']}
                            else :              token = {'form':'<DRUG_OTHER>', 'lc_form':'<DRUG_OTHER>', 'lemma':'<DRUG_OTHER>', 'pos':'<DRUG_OTHER>', 'etype':entities[tk_ent]['type']}
                        
                            if tk_ent==None or tk_ent not in seen : sent.append(token)
                            if tk_ent!=None : seen.add(tk_ent)
                        
                        # resulting vector
                        self.data.append({'sid': sid, 'e1':e1, 'e2':e2, 'type':dditype, 'sent':sent})                    

    ## ---- iterator to get sentences in the data set
    def save(self, filename) :
        with open(filename+".pck", "wb") as pf:
            pickle.dump(self.data, pf)

                        
    ## ---- iterator to get sentences in the data set
    def sentences(self) :
        for s in self.data :
            yield s

