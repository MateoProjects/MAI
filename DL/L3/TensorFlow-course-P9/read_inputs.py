import tarfile
import re
import copy
import pickle
import argparse
import os.path
import sys
import time
import gzip
import configparser
import csv
import numpy as np

def load_data_mnist(dataset):
    f = gzip.open(dataset, 'rb')
    train_set, valid_set, test_set = pickle.load(f, encoding='latin1')
    f.close()

    n_in = 28
    in_channel = 1
   
    test_set_x, test_set_y = test_set
    valid_set_x, valid_set_y = valid_set
    train_set_x, train_set_y = train_set

    rval = [(train_set_x, train_set_y), (valid_set_x, valid_set_y), (test_set_x, test_set_y)]
    return rval, n_in, in_channel, 10


def load_data_cifar10(dataset):
    train_dic = dict()
    f = tarfile.open(dataset, 'r')
    for member in f.getmembers():
        match1 = re.search(r".*\/data_batch_.*", member.name)
        match2 = re.search(r".*\/test_batch", member.name)
        if match1 is not None:
            print("Training: extracting {} ...".format(member.name))
            ef = f.extractfile(member)
            train_tmp = pickle.load(ef, encoding='latin1')
            if bool(train_dic) is False:
                train_dic = train_tmp
            else:
                train_dic['data'] = np.append(train_dic['data'], train_tmp['data'], axis=0)
                train_dic['labels'] = np.append(train_dic['labels'], train_tmp['labels'], axis=0)
        elif match2 is not None:
            print("Testing/Validating: extracting {} ...".format(member.name))
            ef = f.extractfile(member)
            test_dic = pickle.load(ef, encoding='latin1')
            test_dic['labels'] = np.array(test_dic['labels'])
    f.close()

    n_in = 32
    in_channel = 3
   
    def shared_dataset(data_dic, borrow=True):
        data_x = data_dic['data'].astype(np.float32)
        data_x /= 255.0#data_x.max()
        data_y = data_dic['labels'].astype(np.int32)
        return data_x, data_y

    train_set_x, train_set_y = shared_dataset(train_dic)
    test_set_x, test_set_y = shared_dataset(test_dic)
    #valid_set_x, valid_set_y = shared_dataset(valid_dic)

    rval = [(train_set_x, train_set_y), (test_set_x, test_set_y), (test_set_x, test_set_y)]
    return rval, n_in, in_channel, 10

