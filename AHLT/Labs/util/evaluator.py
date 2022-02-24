#! /usr/bin/python3

import sys
from os import listdir

from xml.dom.minidom import parse

## --
## -- auxliary to insert an instance in given instance_set
## --

def add_instance(instance_set, einfo, etype) :
    instance_set["CLASS"].add(einfo+"|"+etype)
    instance_set["NOCLASS"].add(einfo)
    if etype not in instance_set : instance_set[etype] = set([])
    instance_set[etype].add(einfo)

    
## --
## -- Load entities from XML files in given golddir
## --

def load_gold_NER(golddir) :
    entities = { "CLASS" : set([]), "NOCLASS" : set([]) }

    # process each file in directory
    for f in listdir(golddir) :

        # parse XML file, obtaining a DOM tree
        tree = parse(golddir+"/"+f)

        # process each sentence in the file
        sentences = tree.getElementsByTagName("sentence")
        for s in sentences :
            sid = s.attributes["id"].value   # get sentence id
            
            # load sentence entities
            ents = s.getElementsByTagName("entity")
            for e in ents :
                einfo = sid + "|" + e.attributes["charOffset"].value  + "|" + e.attributes["text"].value
                etype = e.attributes["type"].value
                add_instance(entities, einfo, etype)
            
    return entities

## --
## -- Load relations from XML files in given golddir
## --

def load_gold_DDI(golddir) :
    relations = { "CLASS" : set([]), "NOCLASS" : set([]) }

    # process each file in directory
    for f in listdir(golddir) :

        # parse XML file, obtaining a DOM tree
        tree = parse(golddir+"/"+f)

        # process each sentence in the file
        sentences = tree.getElementsByTagName("sentence")
        for s in sentences :
            sid = s.attributes["id"].value   # get sentence id
        
            # load "pairs"  in the sentence, keep those with ddi=true
            pairs = s.getElementsByTagName("pair")
            for p in pairs:
                id_e1 = p.attributes["e1"].value
                id_e2 = p.attributes["e2"].value
                ddi = p.attributes["ddi"].value

                if (ddi == "true") :
                    rtype = p.attributes["type"].value
                    rinfo = sid + "|" + id_e1 + "|" +  id_e2
                    add_instance(relations, rinfo, rtype)

    return relations


## --
## -- Load entities/relations from given system output file
## --

def load_predicted(task, outfile) :
    predicted = { "CLASS" : set([]), "NOCLASS" : set([]) }
    outf = open(outfile,"r")
    for line in outf.readlines() :
        line = line.strip()
        if line in predicted["CLASS"] :
            print("Ignoring duplicated entity in system predictions file: "+line)
            continue

        etype = line.split("|")[-1]
        einfo = "|".join(line.split("|")[:-1])
        add_instance(predicted, einfo, etype)
        outf.close()
        
    return predicted
    


## --
## -- Compare given sets and compute tp,fp,fn,P,R,F1
## --

def statistics(gold,predicted,kind) :
    tp = 0
    fp = 0
    nexp = len(gold[kind])
    if kind in predicted:
        npred = len(predicted[kind])
        for p in predicted[kind] :
            if p in gold[kind] : tp += 1
            else : fp += 1

        fn = 0
        for p in gold[kind] :
            if p not in predicted[kind] : fn += 1

    else :
        npred = 0
        fn = nexp

    P = tp/npred if npred!=0 else 0
    R = tp/nexp if nexp!=0 else 0    
    F1 = 2*P*R/(P+R) if P+R!=0 else 0

    return tp,fp,fn,npred,nexp,P,R,F1

## --
## -- Compute and print statistics table
## --

def row(txt) :
   return txt + ' '*(17-len(txt))


def print_statistics(gold,predicted) :
    print(row("")+"  tp\t  fp\t  fn\t#pred\t#exp\tP\tR\tF1")
    print("------------------------------------------------------------------------------")
    (nk,sP,sR,sF1) = (0,0,0,0)
    for kind in sorted(gold) :
        if kind=="CLASS" or kind=="NOCLASS" : continue
        (tp,fp,fn,npred,nexp,P,R,F1) = statistics(gold, predicted, kind)
        print(row(kind)+"{:>4}\t{:>4}\t{:>4}\t{:>4}\t{:>4}\t{:2.1%}\t{:2.1%}\t{:2.1%}".format(tp,fp,fn,npred,nexp, P, R, F1))
        (nk,sP,sR,sF1) = (nk+1, sP+P, sR+R, sF1+F1)

    (sP, sR, sF1) = (sP/nk, sR/nk, sF1/nk)
    print("------------------------------------------------------------------------------")
    print(row("M.avg")+"-\t-\t-\t-\t-\t{:2.1%}\t{:2.1%}\t{:2.1%}".format(sP, sR, sF1))

    print("------------------------------------------------------------------------------")
    (tp,fp,fn,npred,nexp,P,R,F1) = statistics(gold, predicted, "CLASS")
    print(row("m.avg")+"{:>4}\t{:>4}\t{:>4}\t{:>4}\t{:>4}\t{:2.1%}\t{:2.1%}\t{:2.1%}".format(tp,fp,fn,npred,nexp, P, R, F1))                        
    (tp,fp,fn,npred,nexp,P,R,F1) = statistics(gold, predicted, "NOCLASS")
    print(row("m.avg(no class)")+"{:>4}\t{:>4}\t{:>4}\t{:>4}\t{:>4}\t{:2.1%}\t{:2.1%}\t{:2.1%}".format(tp,fp,fn,npred,nexp, P, R, F1))               

## --
## -- Evaluates results in outfile comparing them with gold standard in golddir.
## -- 'task' is either NER or DDI
## -- This function can be called from any program requesting evaluation.
## --
 
def evaluate(task, golddir, outfile):

    if task=="NER" :
        # get set of expected entities in the whole golddir
        gold = load_gold_NER(golddir)
    elif task == "DDI" :
        # get set of expected relations in the whole golddir
        gold = load_gold_DDI(golddir)
    else :
        print ("Invalid task '"+task+"'. Please specify 'NER' or 'DDI'.")        


    # Load entities/relations predicted by the system
    predicted = load_predicted(task, outfile)

    # compare both sets and compute statistics
    print_statistics(gold,predicted)
         
        
## --
## -- Usage as standalone program:  evaluator.py (NER|DDI) golddir outfile
## --
## -- Evaluates results in outfile comparing them with gold standard in golddir
## --


if __name__ == "__main__":

    if len(sys.argv) != 4 :
        print("\n  Usage: evaluator.py (NER|DDI) golddir outfile\n")
        exit()
        
    task = sys.argv[1]
    golddir = sys.argv[2]
    outfile = sys.argv[3]

    evaluate(task, golddir, outfile)
