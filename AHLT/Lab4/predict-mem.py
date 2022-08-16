#!/usr/bin/env python3

import sys
from MEmodel import *


if __name__ == '__main__':

    # load ME model
    model = MEmodel(sys.argv[1])
    
    # Read instances from STDIN, and classify them
    for line in sys.stdin:
        
        fields = line.strip('\n').split("\t")
        (sid,e1,e2) = fields[0:3]        
        prediction = model.best_class(fields[4:])

        if prediction != "null" :            
            print(sid,e1,e2,prediction,sep="|")
        
