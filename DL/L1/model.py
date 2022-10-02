import tensorflow as tf
import tensorflow.keras.applications as app
import keras
import matplotlib.pyplot as plt
import numpy as np
import cv2
import random
from keras import layers, regularizers
from keras import backend as K
from tensorflow.keras import optimizers
from keras.models import Sequential
from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Dense,  GlobalAveragePooling2D
from tensorflow.keras.utils import Sequence
from tensorflow.keras import utils
from tensorflow.keras.models import Model
from skimage import io
from keras.utils.data_utils import Sequence
from copy import copy
from constants import *


def get_baseModel():
    """
    Get the model from the base model.
    @return model
    """

    model = keras.Sequential()
    model.add(layers.Conv2D(16, kernel_size=(3, 3), activation='gelu', kernel_initializer='he_uniform', padding='same', input_shape=(256,256,3), data_format='channels_last'))
    model.add(layers.BatchNormalization(center=True,))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Conv2D(32, kernel_size=(3, 3), activation='gelu', kernel_initializer='he_uniform', padding='same'))
    model.add(layers.Dropout(0.2))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Conv2D(64, kernel_size=(3, 3), activation='gelu', kernel_initializer='he_uniform',padding='same'))
    model.add(layers.BatchNormalization(center=True,))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Flatten())
    #model.add(layers.Dense(256, activation='gelu'))
    #model.add(layers.Dropout(0.2))
    model.add(layers.Dense(128, activation='gelu' ))
    model.add(layers.Dropout(0.5))
    model.add(layers.BatchNormalization(center=True,))
    model.add(layers.Dense(NUM_CLASSES, activation='softmax'))
    model.summary()
    return model

def recall_m(y_true, y_pred):
    """
    Compute recall of the model given the true labels and the predicted labels.
    :param y_true: true labels
    :param y_pred: predicted labels
    :return: recall
    """
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_m(y_true, y_pred):
    """
    Computes precision for the model given the true labels and the predicted labels.
    @param y_true: true labels
    @param y_pred: predicted labels
    @return: precision
    """
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1_metric(y_true, y_pred):
    """
    Computes the F1 score of the model given the true labels and the predicted labels.
    @param y_true: true labels
    @param y_pred: predicted labels
    @return: F1 score
    """
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))

def print_results_model(mdl_fit, epochs=16, batch_size=32, balanced=True):
    """
    Print the results of the model trained on the given data.
    @param mdl_fit: model trained on the given data
    @param epochs: number of epochs used for training
    @param batch_size: batch size used for training
    @param balanced: whether the data is balanced or not
    """
    # plot the loss
    plt.plot(mdl_fit.history['loss'], label='train loss')
    plt.plot(mdl_fit.history['val_loss'], label='val loss')
    plt.legend()
    plt.savefig("data_epochs_" +str(epochs)+"_batchSize_"+ str(batch_size)+'_LossVal_loss')
    plt.show()
    # plot the accuracy
    plt.plot(mdl_fit.history['accuracy'], label='train acc')
    plt.plot(mdl_fit.history['val_accuracy'], label='val acc')
    plt.legend()
    plt.savefig("balanced_data_epochs_" +str(epochs)+"_batchSize_"+ str(batch_size)+'_AccVal_acc')
    #save model to disk
    plt.show()

def predict_model(model, x_test, y_test,):
  """
  Predict the labels of the test data.
  @param model: model to be used for prediction
  @param x_test: test data
  @param y_test: true labels of the test data
  @return: Correct predicted labels in the given model in percentage
  """
  correct_predicctions = 0
  for i in range(len(x_test)):
    img = x_test[i]
    prediction = model.predict(img)
    if prediction[0][np.argmax(y_test[i])] == 1:
      correct_predicctions += 1
  return correct_predicctions/len(x_test)

def get_valSet(x_test, y_test):
    """
    Gets the validation set.
    :param x_test: test set
    :param y_test: test labels
    :return: validation set
    """
    val_data_gen_args = dict(rescale = None,
                     samplewise_center=True,
                     samplewise_std_normalization=True)
   
    val_datagen = ImageDataGenerator(val_data_gen_args)
    val_set = val_datagen.flow(x_test, y_test, batch_size=BATCH_SIZE)
    return val_set

    