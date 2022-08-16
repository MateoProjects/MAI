#! /usr/bin/python3


from email.mime import base
import sys
import random
from contextlib import redirect_stdout

from tensorflow.keras import regularizers, Input
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Embedding, Dense, Dropout, Conv1D, MaxPool1D, Reshape, Concatenate, Flatten, Bidirectional, LSTM

from transformers import AutoModel, AutoConfig, AutoTokenizer
import torch
from torch import nn
from tqdm import tqdm
import time

from dataset import *
from codemaps import *

BASE_MODEL_NAME = "distilbert-base-uncased"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MAX_LEN = 174
EMBEDDING_SIZE = 768


def create_tokenizer():
   tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME)
   tokenizer.add_tokens(['<DRUG1>', '<DRUG2>', '<DRUG_OTHER>'])

   return tokenizer

class OurDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        inputs = {key: val[idx].to(DEVICE) for key, val in self.encodings.items()}
        labels = self.labels[idx].to(DEVICE)
        return inputs, labels

    def __len__(self):
        return len(self.labels)

def create_dataloader(codes, tokenizer, dataset, batch_size=32, shuffle=True, pin_memory=False):
   # Get data
   list_sentences = []
   for s in dataset.sentences():
      sentence = ""
      for w in s["sent"]:
         sentence += f"{w['form']} "
      list_sentences.append(sentence)

   # Tokenize data   
   encodings = tokenizer(list_sentences, max_length=MAX_LEN, truncation=True, padding="max_length", return_tensors='pt')

   # Get labels
   labels = torch.Tensor(codes.encode_labels(dataset))
   
   # Create dataset and dataloader
   our_dataset = OurDataset(encodings, labels)   
   dataloader = torch.utils.data.DataLoader(our_dataset, batch_size=batch_size, shuffle=shuffle, pin_memory=pin_memory)

   return dataloader

class OurNet(nn.Module):
    def __init__(self, base_model, n_labels):
        super(OurNet, self).__init__()
        self.base_model = base_model
        self.n_labels = n_labels
        self.seq = nn.Sequential(
            #nn.Conv1d(in_channels=EMBEDDING_SIZE, out_channels=64, kernel_size=1, padding="same"),
            #nn.ReLU(),
            nn.Conv1d(in_channels=EMBEDDING_SIZE, out_channels=32, kernel_size=2, padding="same"),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(MAX_LEN*32, n_labels),
            nn.Softmax(dim=-1),
        )

    def forward(self, input):
         x = self.base_model(**input)
         x = x.last_hidden_state
         x = torch.reshape(x, (x.shape[0], x.shape[2], x.shape[1]))  # Batch, channels, length
         x = self.seq(x)
         return x

def build_our_network(codes, tokenizer):
   n_labels = codes.get_n_labels()

   # Create BERT-based model for embeddings
   base_model = AutoModel.from_pretrained(BASE_MODEL_NAME)
   base_model.resize_token_embeddings(len(tokenizer))

   # Freeze base model parameters   
   #for param in base_model.parameters():
   #   param.requires_grad = False
   
   # Create complete model
   model = OurNet(base_model, n_labels)
   model = model.to(DEVICE)

   return model

def build_network():
   # sizes
   n_words = codes.get_n_words()
   max_len = codes.maxlen
   n_labels = codes.get_n_labels()

   # word input layer & embeddings
   inptW = Input(shape=(max_len,))
   embW = Embedding(input_dim=n_words, output_dim=100,
                      input_length=max_len, mask_zero=False)(inptW)  

   conv = Conv1D(filters=30, kernel_size=2, strides=1, activation='relu', padding='same')(embW)
   flat = Flatten()(conv)
   
   out = Dense(n_labels, activation='softmax')(flat)

   model = Model(inptW, out)
   model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

   return model

def train(model, train_dataloader, val_dataloader, optimizer, criterion, epochs):
   for epoch in range(epochs):
      base_desc = f"[Epoch {epoch+1}/{epochs}]"
      train_loss = 0.0
      num_correct_train = 0
      model.train()
      with tqdm(iter(train_dataloader), total=len(train_dataloader), desc=base_desc+" training") as pbar:
         for i, data in enumerate(pbar):
            # get the inputs; data is a list of [inputs, labels]
            inputs, labels = data         

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # Accumulate loss
            train_loss += loss.item()

            # Count num correct
            batch_preds = torch.argmax(outputs, dim=-1)
            batch_labels = torch.argmax(labels, dim=-1)
            num_correct_train += torch.count_nonzero(batch_preds == batch_labels)

            # Update progress bar
            pbar.update()
            pbar.set_description(base_desc+f" training | loss = {train_loss/(i+1):e}")

      # Evaluate on validation dataset
      val_loss = 0
      num_correct_val = 0
      model.eval()
      with tqdm(iter(val_dataloader), total=len(val_dataloader), desc=f"Epoch {epoch+1}/{epochs} validation") as pbar:
         for i, data in enumerate(pbar):
            inputs, labels = data
            outputs = model(inputs)
            val_loss += criterion(outputs, labels).item()
            batch_preds = torch.argmax(outputs, dim=-1)
            batch_labels = torch.argmax(labels, dim=-1)
            num_correct_val += torch.count_nonzero(batch_preds == batch_labels)

            # Update progress bar
            pbar.update()
            pbar.set_description(base_desc+f" validation | loss = {val_loss/(i+1):e}")

      # Epoch statistics
      train_accuracy = num_correct_train / len(train_dataloader.dataset)
      val_accuracy = num_correct_val / len(val_dataloader.dataset)
      avg_train_loss = train_loss / len(train_dataloader.dataset)
      avg_val_loss = val_loss / len(val_dataloader.dataset)
      print(f"[Epoch {epoch + 1}/{epochs}] loss: {avg_train_loss:e} accuracy = {train_accuracy} | val_loss: {avg_val_loss:e} val_accuracy: {val_accuracy}")


## --------- MAIN PROGRAM ----------- 
## --
## -- Usage:  train.py ../data/Train ../data/Devel  modelname
## --

## --------- MAIN PROGRAM ----------- 
## --
## -- Usage:  train.py ../data/Train ../data/Devel  modelname
## --

if __name__ == "__main__":
   # directory with files to process
   trainfile = sys.argv[1]
   validationfile = sys.argv[2]
   modelname = sys.argv[3]

   # load train and validation data
   traindata = Dataset(trainfile)
   valdata = Dataset(validationfile)

   # create indexes from training data
   max_len = 50
   codes = Codemaps(traindata, max_len)

   """# build network
   model = build_network()
   with redirect_stdout(sys.stderr):
      model.summary()

   # encode datasets
   Xt = codes.encode_words(traindata)
   Yt = codes.encode_labels(traindata)

   Xv = codes.encode_words(valdata)
   Yv = codes.encode_labels(valdata)

   # train model
   with redirect_stdout(sys.stderr):
      model.fit(Xt, Yt, batch_size=32, epochs=10, validation_data=(Xv,Yv), verbose=1)
   """

   # encode datasets
   tokenizer = create_tokenizer()
   train_dataloader = create_dataloader(codes, tokenizer, traindata)
   val_dataloader = create_dataloader(codes, tokenizer, valdata)

   # build network
   model = build_our_network(codes, tokenizer)

   # train model
   optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
   #class_weights = torch.Tensor([1, 1, 1, 1, 0.5])
   #class_weights = class_weights.to(DEVICE)
   criterion = nn.CrossEntropyLoss()
   train(model, train_dataloader, val_dataloader, optimizer, criterion, epochs=1)

   # save model and indexs
   #model.save(modelname)
   torch.save(model, modelname)
   codes.save(modelname)

