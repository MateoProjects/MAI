#####################################################
## Class to store an ngram ME model
#####################################################

import pycrfsuite

class CRF:

    ## --------------------------------------------------
    ## Constructor: Load model from file
    ## --------------------------------------------------
    def __init__(self, datafile):
        # Create a CRF Tagger object, and load given model
        self.tagger =  pycrfsuite.Tagger()
        self.tagger.open(datafile)
        
    ## --------------------------------------------------
    ## predict best class for each element in xseq
    ## --------------------------------------------------
    def predict(self, xseq):
        return self.tagger.tag(xseq)
