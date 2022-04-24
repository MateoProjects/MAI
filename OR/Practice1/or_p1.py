# -*- coding: utf-8 -*-
"""OR_p1.ipynb

# Data Augmentation

* Ramon Mateo Navarro

## IMPORTS & CONSTANTS
"""

from glob import glob
import cv2
import numpy as np
import xml.etree.ElementTree as ET
import keras
import random
from keras import backend as K
from tensorflow.keras import optimizers
from keras.models import Sequential
from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Dense, Activation, Flatten, Dropout, BatchNormalization, GlobalAveragePooling2D
from keras.layers import Conv2D, MaxPooling2D
from keras import regularizers
from keras.callbacks import LearningRateScheduler
from skimage.transform import rotate , resize
from skimage import io
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import os
import numpy as np
PATH_FOLDER = "VOCdevkit"


batch_size = 128
n_epochs = 12
per_sample_normalization = True
data_augmentation = False
globalAVGPooling = True
drop_out = True
capacity = ['low', 'high'][1]
last_layer_activation = ['softmax', 'sigmoid', None][1]
net_name = [['resnet50','ResNet50'], ['inception_v3','InceptionV3'], ['mobilenet_v2','MobileNetV2']][0]
loss = ['categorical_crossentropy', 'binary_crossentropy', 'mean_squared_error', 'mean_absolute_error'][1]
txt = 'rnd'
img_size = 224
num_classes = 20
img_with_padding = False
voc_classes = {'aeroplane': 0, 'bicycle': 1, 'bird': 2, 'boat': 3, 'bottle': 4, 'bus': 5, 'car': 6, 'cat': 7, 'chair': 8, 'cow': 9, 'diningtable': 10, 'dog': 11, 'horse': 12, 'motorbike': 13, 'person': 14, 'pottedplant': 15, 'sheep': 16, 'sofa': 17, 'train': 18, 'tvmonitor': 19}
IMAGES_DICT = {'aeroplane': [], 'bicycle': [], 'bird':[], 'boat': [], 'bottle': [], 'bus': [], 'car': [], 'cat': [], 'chair': [], 'cow': [], 'diningtable': [], 'dog': [], 'horse': [], 'motorbike': [], 'person': [], 'pottedplant': [], 'sheep': [], 'sofa': [], 'train': [], 'tvmonitor': []}

def read_content(xml_file):
  tree = ET.parse(xml_file)
  root = tree.getroot()

  list_with_all_boxes = []
  list_with_all_objects = []
  for boxes in root.iter('object'):

      classname = boxes.find("name").text
      list_with_all_objects.append(voc_classes[classname])

      ymin, xmin, ymax, xmax = None, None, None, None

      ymin = int(boxes.find("bndbox/ymin").text)
      xmin = int(boxes.find("bndbox/xmin").text)
      ymax = int(boxes.find("bndbox/ymax").text)
      xmax = int(boxes.find("bndbox/xmax").text)

      list_with_single_boxes = [xmin, ymin, xmax, ymax]
      list_with_all_boxes.append(list_with_single_boxes)

  return list_with_all_objects, list_with_all_boxes


files = glob('VOCdevkit/VOC2007/JPEGImages/*.jpg')

n_samples = len(files)
files = files[:n_samples]

np.random.seed(0)
ridx = np.random.randint(0, n_samples, int(n_samples*0.2))
train_test_split = np.zeros(n_samples)
train_test_split[ridx] = 1


def read_files():
  x_train, y_train, x_test, y_test = [], [], [], []
  print("##### READING CONTENT #####")

  for f, i in zip(files, range(n_samples)):
      img = cv2.imread(f)
      img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32)
      if img_with_padding:
          catdim = 0
          if img.shape[0] > img.shape[1]:
              cataxis = 1
              catdim = int((img.shape[0] - img.shape[1]) / 2)
              catarray = np.zeros((img.shape[0], catdim, img.shape[2]), img.dtype)
              img = np.concatenate((catarray, img, catarray), axis=cataxis)
          elif img.shape[0] < img.shape[1]:
              cataxis = 0
              catdim = int((img.shape[1] - img.shape[0]) / 2)
              catarray = np.zeros((catdim, img.shape[1], img.shape[2]), img.dtype)
              img = np.concatenate((catarray, img, catarray), axis=cataxis)
      img = cv2.resize(img, (img_size, img_size))
      
      if train_test_split[i]:
          x_test.append(img)
      else:
          x_train.append(img)
      
      classes = np.zeros(num_classes)
      root, name = f.split('JPEGImages', 1)
      cnames, bounding_boxes = read_content(root+'Annotations'+name[:-3]+'xml')
      for c in cnames:
          classes[c] = 1.0
              
      if train_test_split[i]:
          y_test.append(classes)
      else:
          y_train.append(classes)
  
  print("##### END READING CONTENT #####")   
  x_train = np.array(x_train)
  y_train = np.array(y_train)
  x_test = np.array(x_test)
  y_test = np.array(y_test)
  return x_train, y_train, x_test, y_test

def check_segmentationData():
  # Check out the segmentation data
  files = glob('VOCdevkit/VOC2007/SegmentationClass/*.png')
  print(len(files))
  im = cv2.imread(files[400])
  im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
  plt.imshow(im)
  plt.show()

  # plot the data distribution
  fig = plt.figure()
  ax = fig.add_axes([0,0,1,1])
  labs = voc_classes.keys()
  data_balance = np.sum(y_train, 0) / y_train.shape[0]
  ax.bar(labs,data_balance)
  plt.xticks([i for i in range(20)], labs, rotation='vertical')
  plt.show()


samples_dA = glob('P1_images/Images/*.jpg') # definir path. JPEG
samples_dA_segmentation = glob('P1_images/Segmentation/*.jpg') # segmentation of Samples
bounding_box = []

def compute_boundingBox(img):
  """
  Compute the bounding box of the image.
  """
  # Compute the bounding box
  x_min = img.shape[1]
  x_max = 0
  y_min = img.shape[0]
  y_max = 0
  for i in range(img.shape[0]):
      for j in range(img.shape[1]):
          if img[i, j].sum() != 0:
              if j < x_min:
                  x_min = j
              if j > x_max:
                  x_max = j
              if i < y_min:
                  y_min = i
              if i > y_max:
                  y_max = i
  return (x_min, x_max, y_min, y_max)
  

def process_img(image, img_seg):
  image[img_seg[:,:] == 0] = 0
  boundingBox = compute_boundingBox(image)
  return image, boundingBox


def getImages():
  images = os.listdir('VOCdevkit/VOC2007/JPEGImages/')
  images_seg = os.listdir('VOCdevkit/VOC2007/SegmentationObject/')
  samples, boundingBoxes = [], []

  for image in images:
    img = image
    if image.replace(".jpg", ".png") in images_seg:
      img = io.imread('VOCdevkit/VOC2007/JPEGImages/'+img)
      index = images_seg.index(image.replace(".jpg", ".png"))
      image_segmentation = io.imread('VOCdevkit/VOC2007/SegmentationObject/'+images_seg[index])
      image_segmentation = rgb2gray(image_segmentation[:,:,:3])
      sample, bounding_box = process_img(img, image_segmentation)
      samples.append(sample)
      boundingBoxes.append(bounding_box)
  return samples, boundingBoxes

def save_data(samples, boundingBoxes):

  print("##### SAVING IMAGES #####")
  for i in range(len(samples)):
    io.imsave("P1_images/ImagesClean/" + str(i) + ".jpg" , samples[i])
  
  np.save("P1_images/boundingBoxes", boundingBoxes)
  print("##### END SAVING IMAGES #####")


def rotate_img(image, angles):
  return rotate(image, angles, resize=True)

def resize_img(image):
   return resize(image, (image.shape[0] // 4, image.shape[1] // 4),anti_aliasing=True)


def find_min_class(clases):
  pass

def dataAugmentation(num_corrup=0.1, random=False, overlap=False, balanced=False):
  if balanced:
    # reduce dataset to minimum of all clases. 
    min = find_min_class(classes)
    # esplitejar les dades per clase i agafar min samples

    pass
  images = np.random.choice(x_train, len(x_train)*num_corrup) # get n random samples for data augmentation

def cut_image(sample, boundingBox):
  """
  Cut the image in the bounding box.
  """
  x_min, x_max, y_min, y_max = boundingBox[0], boundingBox[1], boundingBox[2], boundingBox[3]
  return sample[y_min:y_max, x_min:x_max]

def cut_images(samples, boundingBoxes):
  images = []
  for i in range (len(samples)):
    image = cut_image(samples[i], boundingBoxes[i])
    images.append(image)
  return images


if __name__ == '__main__':
  x_train, y_train, x_test, y_test =  read_files()
  samples, bounding_box = getImages()
  print(type(y_train[0]))
  samples = cut_images(samples, bounding_box)
  save_data(samples, bounding_box)
  img = rotate_img(samples[0], random.randint(0,360))
  plt.imshow(img)
  plt.show()