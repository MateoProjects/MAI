#####################################################
## Class to store an ngram MLE model
#####################################################

class MLEmodel:


    ## --------------------------------------------------
    ## Constructor: Load model from file
    ## --------------------------------------------------
    def __init__(self, datafile=None):

        self.uni_count = {}  # set of observed unigrams, with counts
        self.trg_count = {} # set of observed trigrams, with counts
        self.big_count = {} # set of observed bigrams, with counts
        self.trg_prob = {}  # set of observed bigrams, with probabilities P(z|xy)
        self.continuations = {}  # number of different z's seen after each bigram xy
        self.total_count = 0 # total number of observed trigrams

        if datafile is not None :
            model = open(datafile, encoding='utf-8')

            # load trigram counts from file
            lin = model.readline(); 
            while (lin != "") :
                (xyz, tcount) = lin.strip().split()
                self.add_trigram_count(xyz, float(tcount))
                
                lin = model.readline();

            model.close() 
            self.recompute()
        
       

    ## --------------------------------------------------
    ## recompute additional tables from current trigram counts
    ## --------------------------------------------------
    def recompute(self) :
        self.trg_prob = {}
        self.continuations = {}
        
        for xyz in self.trg_count :
            
            xy = xyz[0:2]
            z = xyz[2]

            # P(z|xy) probability
            self.trg_prob[xyz] = float(self.trg_count[xyz])/float(self.big_count[xy])

            # number of different z's seen after xy
            if xy in self.continuations : self.continuations[xy] += 1
            else : self.continuations[xy] = 1


            
    ## --------------------------------------------------
    ## add 'tcount' to the number of times xyz, xy, and z have been seen
    ## --------------------------------------------------
    def add_trigram_count(self, xyz, tcount) :
        xy = xyz[0:2]
        z = xyz[2]
        
        # increase trigram counts for xyz
        if xyz in self.trg_count : self.trg_count[xyz] += tcount
        else : self.trg_count[xyz] = tcount

        # increase bigram counts for xy
        if xy in self.big_count : self.big_count[xy] += tcount
        else : self.big_count[xy] = tcount

        # increase unigram counts for z
        if z in self.uni_count : self.uni_count[z] += tcount
        else : self.uni_count[z] = tcount

        # total number of observations
        self.total_count += tcount

        
    ## --------------------------------------------------
    ## print the model to a file, for later use
    ## --------------------------------------------------
    def dump(self) :        
        for xyz in sorted(self.trg_count) :
            print(xyz, self.trg_count[xyz])


    ## --------------------------------------------------
    ## compute porbability distribution for all possible z after xy
    ## --------------------------------------------------
    def prob_dist_z(self, xy) :        
        p = {}

        for z in self.uni_count :
            p[z] = self.conditional_prob(xy,z)

        return p

    
    ## ---------------------------------
    ## trigram probability P(z|xy), unsmoothed

    def conditional_prob(self, xy, z) :
        if xy+z in self.trg_prob :
            return self.trg_prob[xy+z]
        else :
            return 0.0

    ## ---------------------------------
    ## Linear discount smoothing (a = alpha parameter)
    def conditional_prob_LD(self, xy, z, a=0.1) :

        B = 80
        if xy in self.continuations : N0 = B - self.continuations[xy]
        else : N0 = B
        if N0<=0 :
            print ("ERROR - Negative N0. Fix estimation of B")
            exit()
    
        # compute p=P(z|xy) using linear discount with alpha=a
        # TO-DO TO-DO
        
        return p

    ## ---------------------------------
    ## Linear discount smoothing with back-off (a = alpha parameter)

    def conditional_prob_LD_bkoff(self, xy, z, a=0.1) :

        B = 80
        N0 = B - len(self.uni_count)
        if N0<=0 :
            print ("ERROR - Negative N0. Fix estimation of B")
            exit()
  
        # compute p=P(z|xy) using linear discount with alpha=a
        # TO-DO TO-DO

        return p

