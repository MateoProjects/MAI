import keras
from keras import backend as K
from tensorflow.keras import optimizers
from keras.models import Sequential
from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Dense,  GlobalAveragePooling2D
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import tensorflow.keras.applications as app
from tensorflow.keras.models import Model
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from keras.utils.data_utils import Sequence
from copy import copy

BATCH_SIZE = 64
EPOCHS = 12
NUM_CLASSES = 20
model = ResNet50(weights='imagenet')
train_from_scratch = False
net_name = [['resnet50','ResNet50'], ['inception_v3','InceptionV3'], ['mobilenet_v2','MobileNetV2']][0]
last_layer_activation = ['softmax', 'sigmoid', None][1]
loss = ['categorical_crossentropy', 'binary_crossentropy', 'mean_squared_error', 'mean_absolute_error'][1]
txt = 'rnd'
per_sample_normalization = True

def get_baseModel():
    """
    Get the model from the base model.
    @return model
    """

    mynet = getattr(getattr(app, net_name[0]), net_name[1])

    # create the base pre-trained model
    if train_from_scratch:
        base_model = mynet(include_top=False)
    else:
        base_model = mynet(weights='imagenet', include_top=False)

    # add a global spatial average pooling layer
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    # let's add a fully-connected layer
    x = Dense(1024, activation='relu')(x)
    # and a logistic layer
    predictions = Dense(NUM_CLASSES, activation=last_layer_activation)(x)

    # this is the model we will train
    model = Model(inputs=base_model.input, outputs=predictions)
    opt_rms = optimizers.RMSprop(learning_rate=0.001, decay=1e-6)
    model.compile(loss=loss, optimizer=opt_rms, metrics=['accuracy'])
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
    if balanced:
        plt.savefig("balanced_data_epochs_" +str(epochs)+"_batchSize_"+ str(batch_size)+'_LossVal_loss')
    else:
        plt.savefig("no_balanced_data_epochs_" + str(epochs) + "_batchSize_" + str(batch_size)+'_LossVal')

    # plot the accuracy
    plt.plot(mdl_fit.history['accuracy'], label='train acc')
    plt.plot(mdl_fit.history['val_accuracy'], label='val acc')
    plt.legend()

    if balanced:
        plt.savefig("balanced_data_epochs_" +str(epochs)+"_batchSize_"+ str(batch_size)+'_AccVal_acc')
    else: 
        plt.savefig("no_balanced_data_epochs_" +str(epochs)+"_batchSize_"+ str(batch_size)+'_AccVal_acc')

    #save model to disk
    model.save_weights('model.h5') 


def get_valSet(x_test, y_test):
    """
    Gets the validation set.
    :param x_test: test set
    :param y_test: test labels
    :return: validation set
    """
    val_data_gen_args = dict(rescale = None if per_sample_normalization else 1./255,
                     samplewise_center=True if per_sample_normalization else False,
                     samplewise_std_normalization=True if per_sample_normalization else False)

    val_datagen = ImageDataGenerator(val_data_gen_args)
    val_set = val_datagen.flow(x_test, y_test, batch_size=BATCH_SIZE)
    return val_set
