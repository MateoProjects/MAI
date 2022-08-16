
import string
import re

import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

from dataset import *

class Codemaps :
    # --- constructor, create mapper either from training data, or
    # --- loading codemaps from given file
    def __init__(self, data, maxlen=None) :
                # Predefined indices for padding and unknown tokens
        self.pad_idx = 0
        self.unk_idx = 1

        # Declare codes (name, function) settings dictionary
        self.codes_settings = {
            #"WORD": lambda tk: tk['form'],
            "LC_WORD": lambda tk: tk['lc_form'],
            "LEMMA": lambda tk: tk['lemma'],
            #"POS": lambda tk: tk['pos'],
            #"ETYPE": lambda tk: tk.get('etype', "NO"),
            #"PREF": lambda tk: tk['lc_form'][:3],
            #"SUFF": lambda tk: tk['lc_form'][-3:],
        }

        if isinstance(data,Dataset) and maxlen is not None :
            self.__create_indexs(data, maxlen)

        elif type(data) == str and maxlen is None :
            self.__load(data)

        else:
            print('codemaps: Invalid or missing parameters in constructor')
            exit()

            
    # --------- Create indexs from training data
    # Extract all words and labels in given sentences and 
    # create indexes to encode them as numbers when needed
    def __create_indexs(self, data, maxlen) :
        self.maxlen = maxlen

        # Create vocabularies
        self.vocabularies = { name: set([]) for name in self.codes_settings.keys() }
        labels = set([])
        for s in data.sentences():
            # Add label
            labels.add(s['type'])
            for tk in s['sent']:                
                # Add tags
                for name, func in self.codes_settings.items():
                    self.vocabularies[name].add(func(tk))
        
        # Create indexes (+1 for padding, +2 for padding and unknown)
        self.labels_indexes = {t:i for i,t in enumerate(sorted(list(labels)))}
        self.codes_indexes = { name: {w: i+2 for i,w in enumerate(list(values_set))} for name, values_set in self.vocabularies.items() }
        
              
    
    ## ---------- Save model and indexs ---------------
    def save(self, name) :
        # save indexes
        with open(name+".idx","w") as f :
            print ('MAXLEN', self.maxlen, "-", file=f)
            for elem, index in self.labels_indexes.items(): print('LABEL', elem, index, file=f)
            for name, code_indexes in self.codes_indexes.items():
                for elem, index in code_indexes.items(): print(name, elem, index, file=f)

    ## --------- load indexs ----------- 
    def __load(self, name) : 
        self.maxlen = 0
        self.codes_indexes = { name: {} for name in self.codes_settings.keys() }
        self.labels_indexes = {}
        
        with open(name+".idx") as f :
            for line in f.readlines():
                (key, elem, index) = line.split()
                if key == 'MAXLEN' : self.maxlen = int(elem)
                elif key == 'LABEL': self.labels_indexes[elem] = int(index)
                elif key in self.codes_indexes.keys():
                    self.codes_indexes[key][elem] = int(index)
                
                
    ## --------- get code for key k in given index, or code for unknown if not found
    def __code(self, index, k) :
        return index[k] if k in index else index['UNK']

    ## --------- encode and pad all sequences of given key (form, lemma, etc) ----------- 
    def __encode_and_pad(self, data, index, key) :
        X = [[self.__code(index,w[key]) for w in s['sent']] for s in data.sentences()]
        X = pad_sequences(maxlen=self.maxlen, sequences=X, padding="post", value=index['PAD'])
        return X
    
    ## --------- encode X from given data -----------    
    def encode_words(self, data):
        # Create encodings
        encodings = []
        for func, code_indexes in zip(self.codes_settings.values(), self.codes_indexes.values()):
            encoded = [[code_indexes.get(func(tk), self.unk_idx) for tk in s["sent"]] for s in data.sentences()]
            encoded = pad_sequences(maxlen=self.maxlen, sequences=encoded, padding="post", value=self.pad_idx)
            encodings.append(encoded)
        
        # return encoded sequences
        return encodings
    
    ## --------- encode Y from given data ----------- 
    def encode_labels(self, data) :
        # encode and pad sentence labels 
        Y = [self.labels_indexes[s['type']] for s in data.sentences()]
        Y = [to_categorical(i, num_classes=self.get_n_labels()) for i in Y]
        return np.array(Y)

    ## -------- get sizes of codes by name ---------
    def get_codes_sizes_dict(self):
        return {name:len(code_indexes) + 2 for name, code_indexes in self.codes_indexes.items()}    # +2 for padding and unknown

    ## -------- get label index size ---------
    def get_n_labels(self) :
        return len(self.labels_indexes)

    ## -------- get index for given label --------
    def label2idx(self, l) :
        return self.labels_indexes[l]
    
    ## -------- get label name for given index --------
    def idx2label(self, i) :
        for l in self.labels_indexes :
            if self.labels_indexes[l] == i:
                return l
        raise KeyError

