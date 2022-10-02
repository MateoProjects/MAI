
import string
import re

import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

from dataset import *

class Codemaps:
    # --- constructor, create mapper either from training data, or
    # --- loading codemaps from given file
    def __init__(self, data, maxlen=None, suflen=None, drugbank_path=None):
        # Predefined indices for padding and unknown tokens
        self.pad_idx = 0
        self.unk_idx = 1

        # Read DrugBank if possible
        if drugbank_path is not None:
            self.drugbank = {}
            with open(drugbank_path) as f:
                for line in f.readlines():
                    (n, t) = line.split("|")
                    self.drugbank[n] = t[:-1]   # Removing last linebreak

        # Declare codes (name, function) settings dictionary
        self.codes_settings = {
            "WORD": lambda tk: tk['lc_form'],
            "SUFFIX": lambda tk: tk['lc_form'][-self.suflen:],
            "PREFIX": lambda tk: tk['lc_form'][:self.suflen],
            "ADDITIONAL_FEATURE": lambda tk: self.get_additional_features(tk),
            "DRUGBANK": lambda tk: self.drugbank.get(tk['form'], "NO"),
        }

        if isinstance(data,Dataset) and maxlen is not None and suflen is not None:
            self.__create_indexs(data, maxlen, suflen)

        elif type(data) == str and maxlen is None and suflen is None:
            self.__load(data)

        else:
            print('codemaps: Invalid or missing parameters in constructor')
            exit()    

    def get_additional_features(self, tk):
        upper = tk['form'].isupper()
        alpha = tk['form'].isalpha()
        digits = bool(re.search(r'\d', tk['form']))
        dash = bool(re.search(r'-|_', tk['form']))
        brackets = bool(re.search(r"(\(|\[|\{)\w+(\)|\]|\})", tk['form']))
        length = len(tk['form'])
        
        return f"{upper}_{alpha}_{digits}_{dash}_{brackets}_{length}"

    # --------- Create indexs from training data
    # Extract all words and labels in given sentences and 
    # create indexes to encode them as numbers when needed
    def __create_indexs(self, data, maxlen, suflen):
        self.maxlen = maxlen
        self.suflen = suflen

        # Create vocabularies
        self.vocabularies = { name: set([]) for name in self.codes_settings.keys() }
        labels = set([])
        for s in data.sentences():
            for tk in s:
                # Add label
                labels.add(tk['tag'])
                # Add tags
                for name, func in self.codes_settings.items():
                    self.vocabularies[name].add(func(tk))
        
        # Create indexes (+1 for padding, +2 for padding and unknown)
        self.labels_indexes = { t: i+1 for i,t in enumerate(list(labels)) }
        self.codes_indexes = { name: {w: i+2 for i,w in enumerate(list(values_set))} for name, values_set in self.vocabularies.items() }    
        
    
    ## ---------- Save model and indexs ---------------
    def save(self, name):
        # save indexes
        with open(name+".idx","w") as f :
            print('MAXLEN', self.maxlen, "-", file=f)
            print('SUFLEN', self.suflen, "-", file=f)
            for elem, index in self.labels_indexes.items(): print('LABEL', elem, index, file=f)
            for name, code_indexes in self.codes_indexes.items():
                for elem, index in code_indexes.items(): print(name, elem, index, file=f)            


    ## --------- load indexs ----------- 
    def __load(self, name) : 
        self.maxlen = 0
        self.suflen = 0
        self.codes_indexes = { name: {} for name in self.codes_settings.keys() }
        self.labels_indexes = {}
        
        with open(name+".idx") as f :
            for line in f.readlines():
                (key, elem, index) = line.split()
                if key == 'MAXLEN' : self.maxlen = int(elem)
                elif key == 'SUFLEN' : self.suflen = int(elem)
                elif key == 'LABEL': self.labels_indexes[elem] = int(index)
                elif key in self.codes_indexes.keys():
                    self.codes_indexes[key][elem] = int(index)             
                

    ## --------- encode X from given data ----------- 
    def encode_words(self, data):
        # Create encodings
        encodings = []
        for func, code_indexes in zip(self.codes_settings.values(), self.codes_indexes.values()):
            encoded = [[code_indexes.get(func(tk), self.unk_idx) for tk in s] for s in data.sentences()]
            encoded = pad_sequences(maxlen=self.maxlen, sequences=encoded, padding="post", value=self.pad_idx)
            encodings.append(encoded)
        
        # return encoded sequences
        return encodings

    
    ## --------- encode Y from given data ----------- 
    def encode_labels(self, data):
        # encode and pad sentence labels
        Y = [[self.labels_indexes[tk['tag']] for tk in s] for s in data.sentences()]
        Y = pad_sequences(maxlen=self.maxlen, sequences=Y, padding="post", value=self.pad_idx)
        return np.array(Y)

    ## -------- get label index size ---------
    def get_n_labels(self) :
        return len(self.labels_indexes) + 1 # +1 for padding

    ## -------- get sizes of codes by name ---------
    def get_codes_sizes_dict(self):
        return {name:len(code_indexes) + 2 for name, code_indexes in self.codes_indexes.items()}    # +2 for padding and unknown
        
    ## -------- get index for given label --------
    def label2idx(self, l) :
        return self.labels_indexes[l]
    
    ## -------- get label name for given index --------
    def idx2label(self, i) :
        for l in self.labels_indexes :
            if self.labels_indexes[l] == i:
                return l
        raise KeyError

