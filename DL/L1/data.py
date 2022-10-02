import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import os
from skimage import io
from tensorflow.keras import utils
from constants import *

def split_data(train, test, validation ):
    names_images_train = train[:,0]
    names_images_test = test[:,0]
    names_images_val = validation[:,0]
    y_train = train[:,1]
    y_test = test[:,1]
    y_val = validation[:,1]
    return (names_images_train, names_images_test, names_images_val, y_train, y_test, y_val)

def load_data(file):
    """
    Split data from csv file in three parts: train, test and validation
    """
    file_labels = pd.read_csv(file)
    file_labels = pd.read_csv(file).to_numpy()
    train = file_labels[file_labels[:, 4] == "train"]
    test = file_labels[file_labels[:,4] == "test"]
    validation = file_labels[file_labels[:,4] == "val"]
    return split_data(train, test, validation)
    #print("Train size: ", len(train), "\nTest size: ", len(test), "\nValidation size: ", len(validation))

def labels_to_dict(labels):
    my_labels = {}
    for i in range(len(labels)):
        my_labels[labels[i,1]] = labels[i,0]
    return my_labels

def load_labels():
    """
    Load labels from csv file
    @return numpy array of labels
    """
    labels = pd.read_csv("MAMe_labels.csv", header=None).to_numpy()
    return labels_to_dict(labels)
    


def load_images(data):
    """
    Load images from name of given in the data
    @param data: numpy array with names of images
    @return numpy array with images
    """
    data_x = []
    for name in data:
        img = io.imread("data_256/" + name)
        data_x.append(img)
 
    return np.array(data_x)
