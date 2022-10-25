import numpy as np
import os
import random
import pandas as pd
from tensorflow import keras
from tensorflow import keras
from tensorflow.keras.preprocessing.image import load_img
from keras import layers
import matplotlib.pyplot as plt
from sklearn import metrics
from PIL import ImageOps



NUM_CLASES = 2
input_dir_test = "ISBI2016_ISIC_Part1_Test_Data/"
target_dir_test = "ISBI2016_ISIC_Part1_Test_GroundTruth/"
img_size = (256, 256)
batch_size = 8

def get_paths(input_dir, target_dir):
  input_img_paths = sorted(
      [
          os.path.join(input_dir, fname)
          for fname in os.listdir(input_dir)
          if fname.endswith(".jpg")
      ]
  )
  target_img_paths = sorted(
      [
          os.path.join(target_dir, fname)
          for fname in os.listdir(target_dir)
          if fname.endswith(".png") and not fname.startswith(".")
      ]
  )

  return input_img_paths, target_img_paths

  #for input_path, target_path in zip(input_img_paths[:10], target_img_paths[:10]):
  #    print(input_path, "|", target_path)
input_test_paths, target_test_paths = get_paths(input_dir_test, target_dir_test)
print(len(input_test_paths), "|", len(target_test_paths))

class DataGenerator(keras.utils.Sequence):
    """Helper to iterate over the data (as Numpy arrays)."""

    def __init__(self, batch_size, img_size, input_img_paths, target_img_paths):
        self.batch_size = batch_size
        self.img_size = img_size
        self.input_img_paths = input_img_paths
        self.target_img_paths = target_img_paths

    def __len__(self):
        return len(self.target_img_paths) // self.batch_size

    def __getitem__(self, idx):
        """Returns tuple (input, target) correspond to batch #idx."""
        i = idx * self.batch_size
        batch_input_img_paths = self.input_img_paths[i : i + self.batch_size]
        batch_target_img_paths = self.target_img_paths[i : i + self.batch_size]
        x = np.zeros((self.batch_size,) + self.img_size + (3,), dtype="float32")
        for j, path in enumerate(batch_input_img_paths):
            img = load_img(path, target_size=self.img_size)
            x[j] = img
            x[j] /= 255
        y = np.zeros((self.batch_size,) + self.img_size + (1,), dtype="uint8")
        for j, path in enumerate(batch_target_img_paths):
            img = load_img(path, target_size=self.img_size, color_mode="grayscale")
            y[j] = np.expand_dims(img, 2)
            # Ground truth labels are 1, 2, 3. Subtract one to make them 0, 1, 2:
            #y[j] -= 1
            y[j] = np.uint8(y[j]/255)
        return x, y


def get_model(img_size, num_classes):
    inputs = keras.Input(shape=img_size + (3,))

    ### [First half of the network: downsampling inputs] ###

    # Entry block
    x = layers.Conv2D(32, 3, strides=2, padding="same")(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    previous_block_activation = x  # Set aside residual

    # Blocks 1, 2, 3 are identical apart from the feature depth.
    for filters in [64, 128, 256]:
        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(filters, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(filters, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.MaxPooling2D(3, strides=2, padding="same")(x)

        # Project residual
        residual = layers.Conv2D(filters, 1, strides=2, padding="same")(
            previous_block_activation
        )
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x  # Set aside next residual

    ### [Second half of the network: upsampling inputs] ###

    for filters in [256, 128, 64, 32]:
        x = layers.Activation("relu")(x)
        x = layers.Conv2DTranspose(filters, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.Activation("relu")(x)
        x = layers.Conv2DTranspose(filters, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.UpSampling2D(2)(x)

        # Project residual
        residual = layers.UpSampling2D(2)(previous_block_activation)
        residual = layers.Conv2D(filters, 1, padding="same")(residual)
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x  # Set aside next residual

    # Add a per-pixel classification layer
    outputs = layers.Conv2D(num_classes, 3, activation="softmax", padding="same")(x)

    # Define the model
    model = keras.Model(inputs, outputs)
    return model


# Free up RAM in case the model definition cells were run multiple times
keras.backend.clear_session()

from sklearn.metrics import accuracy_score, recall_score

def get_values(y_true, y_pred):
    # True Positives
    tp = np.sum(np.logical_and(y_pred == 1, y_true == 1))
    # True Negatives
    tn = np.sum(np.logical_and(y_pred == 0, y_true == 0))
    # False Positives
    fp = np.sum(np.logical_and(y_pred == 1, y_true == 0))
    # False Negatives
    fn = np.sum(np.logical_and(y_pred == 0, y_true == 1))
    return tn, fp, fn, tp

def sensitivity(y_true, y_pred):
    return metrics.recall_score(y_true, y_pred, zero_division=0,average='micro')



def specificity(y_true , y_pred, epsilon=1e-20):
    tn, fp, _, _ = get_values(y_true, y_pred)
    res = (tn)/(tn+fp+epsilon)
    return res

def accuracy(y_true, y_pred, epsilon=1e-20):
    tn, fp, fn, tp = get_values(y_true, y_pred)
    res = (tp+tn)/(tp+fp+tn+fn+epsilon)
    return res

def jaccard(y_true, y_pred):
    return metrics.jaccard_score(y_true, y_pred, zero_division=0, average='micro')

def dice_coef(y_true, y_pred, epsilon=1e-20):
    _ , fp, fn, tp = get_values(y_true, y_pred)
    res = (2*tp)/(2*tp+fp+fn+epsilon)
    return res
test_generator = DataGenerator(1, (256,256),input_test_paths, target_test_paths)

model = get_model((256,256), NUM_CLASES)
#model.summary()
paths = ["adam_bat8_30_epoc_noDA.h5", "adam_bat16_30_epoc_DA.h5", "adam_bat16_30_epoc_noDA.h5", 
           "rmsprop_bat8_30_epoch_noDA.h5", "rmsprop_bat16_30_epoc_DA.h5",  "rmsprop_bat16_30_epoch_noDA.h5"]

columns = ['Name', 'Sensitivity', 'Specificity', 'Accuracy', 'jaccard', 'dice_val']
values = []
for path in paths:
    model.load_weights(path)
    results = model.predict(test_generator)
    print("############################################")
    print(path)
    print("############################################")
    #print("Results",results)
    #print("Len is:", len(results))
    #print(results.shape)
    sensitivity_val = 0
    accuracy_val = 0
    specificity_val = 0
    jaccard_val = 0
    dice_val = 0


    for i in range(len(results)):
        img = results[i]
        img_true = np.array(load_img(target_test_paths[i],target_size=(256,256),color_mode="grayscale"))
        img_true = img_true/255
        img_true = np.around(img_true)
        mask = np.argmax(img, axis=-1)
        mask = np.expand_dims(mask, axis=-1)
        img = keras.preprocessing.image.array_to_img(mask)
        img = np.array(img)
        img = np.around(img)
        img = img/255
        sensitivity_val += sensitivity(img_true, img)
        specificity_val += specificity(img_true, img)
        accuracy_val += accuracy(img_true, img)
        jaccard_val += jaccard(img_true,img)
        dice_val += dice_coef(img_true, img)
    values.append([path, sensitivity_val/len(results), specificity_val/len(results), accuracy_val/len(results), jaccard_val/len(results), dice_val/len(results)])
    print("Sensitivity:", sensitivity_val/len(results))
    print("Specificity:", specificity_val/len(results))
    print("Accuracy:", accuracy_val/len(results))
    print("jaccard:", jaccard_val/len(results))
    print("dice_val:", dice_val/len(results))
data = pd.DataFrame(columns=columns, data=values)

data.to_csv("results.csv")