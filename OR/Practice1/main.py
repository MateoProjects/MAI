from glob import glob
import cv2
import numpy as np
import xml.etree.ElementTree as ET
import random
from skimage.transform import rotate , resize
from skimage import io
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import os
import numpy as np
import json
from data_augmentation import *
from utils import *
from model import *

epochs = [8, 16, 32]
batch_sizes = [16, 32, 64]

def save_data(samples, boundingBoxes, images_dict, data):
  """
  Save data to path
  @param samples: numpy array of samples
  @param boundingBoxes: numpy array of bounding boxes
  @param images_dict: dictionary of images
  @param data: dictionary of data
  """
  json.dump(images_dict, open('P1_images/dict_images.json', 'w'))
  np.save('P1_images/data', data)

  print("##### SAVING IMAGES #####")
  for i in range(len(samples)):
    io.imsave("P1_images/ImagesClean/" + str(i) + ".jpg" , samples[i], check_contrast=False)
  
  np.save("P1_images/boundingBoxes", boundingBoxes)
  print("##### END SAVING IMAGES #####")

def save_images(train_x):
  """
  Save images to path
  @param train_x: numpy array of images
  """
  for i in range(len(train_x)):
    io.imsave("P1_images/Images_tr/" + str(i) + ".jpg" , train_x[i], check_contrast=False)

def load_data():
  """
  Loads image and y_train from path and returns it as a numpy array
  @return numpy array of images and labels
  """
  images = []
  files = glob('P1_images/Images_tr/*.jpg')
  for file in files:
    images.append(io.imread(file))
  y_train = np.load("P1_images/train_y.npy")
  print("At this point len of images is: ", len(images))
  print("At this point len of train_y is: ", len(y_train))
  return np.array(images), y_train


if __name__ == '__main__':

  data, images_dict =  read_files() # data = x_train, y_train, x_test, y_test
  list_im_object , list_classes, list_im_rgb = get_objects()

  save_images(data[0])
  train_y = preprocessing(images_dict, list_classes, list_im_rgb, list_im_object,len(data[0]),balanced=True, rand_trans=True)  
  
  plot_balance_data(np.concatenate((data[1], train_y), axis=0), balance=True)

  train_y = np.concatenate((data[1], train_y), axis=0)
  np.save("P1_images/train_y.npy", train_y)
  x_train, y_train = load_data()
  val_set = get_valSet(data[2], data[3])
  for epoch in epochs:
    for batch_size in batch_sizes:
      model = get_baseModel()
      model_fit = model.fit(data[0], data[1], validation_data=val_set, epochs=epoch, batch_size=batch_size)  
      print_results_model(model_fit, balanced=True, batch_size=batch_size, epochs=epoch)