#####################################################
## Class to store an ngram ME model
#####################################################

from math import exp


class MEmodel:

    ## --------------------------------------------------
    ## Constructor: Load model from file
    ## --------------------------------------------------
    def __init__(self, datafile):

        # open file
        model = open(datafile, encoding='utf-8')

        # read first line, class names 
        lin = model.readline()
        self.classes = lin.strip().split()[1:]

        self.lbda = {}
        # load rest of lines into lbd
        lin = model.readline(); 
        while (lin!="") :
            lin = lin.strip().split()
            # first field is the feature name
            feat = lin.pop(0) 
            # rest of fields are lambdas for each class
            for i in range(len(lin)) :
                key = feat + "#" + self.classes[i]
                self.lbda[key] = float(lin[i])

            lin = model.readline(); 

            
    ## --------------------------------------------------
    ## compute porbability distribution for all possible classes given features in 'feats'
    ## --------------------------------------------------
    def prob_dist_z(self,feats) :

        p={}
        z=0        
        for c in self.classes :
            ## add lambda_i * f_i for each example feature
            s=0 
            for f in feats :
                if f+"#"+c in self.lbda:
                    s = s + self.lbda[f+"#"+c]

            p[c] = exp(s)
            z = z + p[c]

        # normalize class probabilities
        for c in self.classes :
            p[c] = p[c]/z

        return p

    ## --------------------------------------------------
    ## compute P(clas|context)
    ## --------------------------------------------------
    def conditional_prob(self, context, clas) :
        dist = self.prob_dist_z(context)
        return dist[clas]
    
    ## --------------------------------------------------
    ## compute argmax P(clas|context)
    ## --------------------------------------------------
    def best_class(self, context) :
        dist = self.prob_dist_z(context)
        return max(dist, key=lambda k: dist[k])
