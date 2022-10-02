#! /usr/bin/python3


import sys
import random
from contextlib import redirect_stdout

from tensorflow.keras import regularizers, Input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Embedding, Dense, Dropout, Conv1D, MaxPool1D, Reshape, concatenate, Flatten, Bidirectional, LSTM

from dataset import *
from codemaps import *

def build_network(codes):
   # sizes
   codes_sizes = codes.get_codes_sizes_dict()

   # Declare inputs, embedding, and dropout layers
   inputs = []
   embeddings = []
   embeddings_dims = {name: 50 for name in codes_sizes.keys()}
   embeddings_dims["LC_WORD"] = 100 # Exception for word
   for name, code_size in codes_sizes.items():
      inpt = Input(shape=(codes.maxlen,))
      inputs.append(inpt)
      embedding = Embedding(input_dim=code_size, output_dim=embeddings_dims[name],
                        input_length=codes.maxlen, mask_zero=False)(inpt)
      #embedding = Dropout(0.1)(embedding)
      embeddings.append(embedding)
   
   # Concatenate embeddings
   if len(embeddings) == 1:
      embeddings = embeddings[0]
   else:
      embeddings = concatenate(embeddings)
   
   # Dropout embeddings
   embeddings = Dropout(0.1)(embeddings)
   
   #embeddings = Bidirectional(LSTM(units=50, return_sequences=True,
   #                           recurrent_dropout=0.1))(embeddings)
   l1_conv1 = Conv1D(filters=30, kernel_size=5, strides=1, activation='relu', padding='same')(embeddings)
   l1_conv2 = Conv1D(filters=30, kernel_size=3, strides=1, activation='relu', padding='same')(embeddings)
   l1_conv = concatenate([l1_conv1, l1_conv2])
   l1_max = MaxPool1D(pool_size=2, strides=1)(l1_conv)
   l2_conv1 = Conv1D(filters=60, kernel_size=5, strides=1, activation='relu', padding='same')(l1_max)
   l2_max = MaxPool1D(pool_size=2, strides=1)(l2_conv1)
   flat = Flatten()(l2_max)
   flat = Dropout(0.1)(flat)
   
   # Output softmax layers
   n_labels = codes.get_n_labels()
   out = Dense(n_labels, activation='softmax')(flat)

   model = Model(inputs, out)
   model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

   return model
   


## --------- MAIN PROGRAM ----------- 
## --
## -- Usage:  train.py ../data/Train ../data/Devel  modelname
## --

## --------- MAIN PROGRAM ----------- 
## --
## -- Usage:  train.py ../data/Train ../data/Devel  modelname
## --


# directory with files to process
trainfile = sys.argv[1]
validationfile = sys.argv[2]
modelname = sys.argv[3]

# load train and validation data
traindata = Dataset(trainfile)
valdata = Dataset(validationfile)

# create indexes from training data
max_len = 40
codes = Codemaps(traindata, max_len)

# build network
model = build_network(codes)
with redirect_stdout(sys.stderr) :
   model.summary()

# encode datasets
Xt = codes.encode_words(traindata)
Yt = codes.encode_labels(traindata)
Xv = codes.encode_words(valdata)
Yv = codes.encode_labels(valdata)

# train model
with redirect_stdout(sys.stderr) :
   model.fit(Xt, Yt, batch_size=32, epochs=10, validation_data=(Xv,Yv), verbose=1)
   
# save model and indexs
model.save(modelname)
codes.save(modelname)

