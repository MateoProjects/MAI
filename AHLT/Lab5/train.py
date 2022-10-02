#! /usr/bin/python3

import sys
from contextlib import redirect_stdout

import tensorflow as tf
import tensorflow.keras as K
from tensorflow.keras import Input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import LSTM, Embedding, Dense, TimeDistributed, Dropout, Bidirectional, concatenate, Lambda, GRU

from dataset import *
from codemaps import *

def weighted_categorical_cross_entropy():
   # Get classes weights
   # labels_index = {'O': 1, 'I-drug_n': 2, 'B-brand': 3, 'B-drug_n': 4, 'B-group': 5, 'B-drug': 6, 'I-group': 7, 'I-drug': 8, 'I-brand': 9, 'PAD': 0}
   # 811500(Total) - 692780(PAD) = 118720 {6: 104876, 4: 2627, 2: 7075, 0: 692780, 9: 530, 3: 1683, 1: 1152, 7: 479, 5: 56, 8: 242}
   tags_frequencies = [0, 1152, 7075, 1683, 2627, 56, 104876, 479, 242, 530]  # PAD freq = 0 to its set weight to 0
   classes_weights = np.array(tags_frequencies)
   classes_weights = np.divide(np.array(1), classes_weights, where=classes_weights!=0) # Inverted weights
   classes_weights = classes_weights / classes_weights[1:].min()  # Normalize by min for obtaining integer values
   #classes_weights = np.array([0, 4, 10, 7, 10, 6, 5, 6, 5, 7])

   # For weights normalization
   min = tf.constant(classes_weights.min(), dtype=tf.float32)
   max = tf.constant(classes_weights.max(), dtype=tf.float32)
   weights_range = max - min

   # Create table for weights mapping
   table = tf.lookup.StaticVocabularyTable(
        tf.lookup.KeyValueTensorInitializer(
            list(range(len(classes_weights))),
            classes_weights,
            key_dtype=tf.int64,
            value_dtype=tf.int64,
        ),
        num_oov_buckets=1,
      )
   
   # Loss function
   def wcce(y_true, y_pred):      
      y_true_weights = table.lookup(tf.cast(y_true, tf.int64)) # [classes_weights[x] for x in y_true]
      y_true_weights = tf.cast(y_true_weights, tf.float32)  # Cast necessary for multiplication
      y_true_weights = (y_true_weights - min) / weights_range # Min-Max normalization
      return K.metrics.sparse_categorical_crossentropy(y_true, y_pred) * y_true_weights
   
   return wcce

def build_network(codes):
   # sizes
   codes_sizes = codes.get_codes_sizes_dict()

   # Declare inputs, embedding, and dropout layers
   inputs = []
   drops = []
   embeddings_dims = {name: 25 for name in codes_sizes.keys()}
   embeddings_dims["WORD"] = 50 # Exception for word
   for name, code_size in codes_sizes.items():
      inpt = Input(shape=(codes.maxlen,))
      inputs.append(inpt)
      embedding = Embedding(input_dim=code_size, output_dim=embeddings_dims[name],
                        input_length=codes.maxlen, mask_zero=True)(inpt)
      drop = Dropout(0.1)(embedding)
      drops.append(drop)
   
   # Concatenate drops
   drops = concatenate(drops)

   # biLSTM
   bilstm = Bidirectional(LSTM(units=100, return_sequences=True,
                               recurrent_dropout=0.1))(drops)
   # output softmax layer
   n_labels = codes.get_n_labels()
   out = TimeDistributed(Dense(n_labels, activation="softmax"))(bilstm)

   # build and compile model
   model = Model(inputs, out)
   model.compile(optimizer="rmsprop",
                 loss="sparse_categorical_crossentropy",
                 metrics=["accuracy"])
   
   return model


## --------- MAIN PROGRAM ----------- 
## --
## -- Usage:  train.py ../data/Train ../data/Devel  modelname
## --
if __name__=="__main__":
   # directory with files to process
   traindir = sys.argv[1]
   validationdir = sys.argv[2]
   modelname = sys.argv[3]
   drugbank_path = sys.argv[4]

   # load train and validation data
   traindata = Dataset(traindir)
   valdata = Dataset(validationdir)

   # create indexes from training data
   max_len = 50
   suf_len = 3
   codes  = Codemaps(traindata, max_len, suf_len, drugbank_path=drugbank_path)
   codes.save(modelname)

   # build network
   model = build_network(codes)
   with redirect_stdout(sys.stderr):
      model.summary()

   # encode datasets
   Xt = codes.encode_words(traindata)
   Yt = codes.encode_labels(traindata)
   Xv = codes.encode_words(valdata)
   Yv = codes.encode_labels(valdata)

   # train model
   with redirect_stdout(sys.stderr):
      model.fit(Xt, Yt, batch_size=16, epochs=10, validation_data=(Xv,Yv), verbose=1)
#      callbacks=[K.callbacks.EarlyStopping(monitor='val_loss', patience=3)])

   # save model and indexs
   model.save(modelname)
   codes.save(modelname)

