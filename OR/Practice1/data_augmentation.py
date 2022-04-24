import numpy as np
import random
import os
import cv2
from skimage import io
from matplotlib import pyplot as plt
from skimage.color import rgb2gray
from skimage.transform import rotate, resize
from glob import glob

NUM_CLASSES = 20
voc_classes = {'aeroplane': 0, 'bicycle': 1, 'bird': 2, 'boat': 3, 'bottle': 4, 'bus': 5, 'car': 6, 'cat': 7, 'chair': 8, 'cow': 9, 'diningtable': 10, 'dog': 11, 'horse': 12, 'motorbike': 13, 'person': 14, 'pottedplant': 15, 'sheep': 16, 'sofa': 17, 'train': 18, 'tvmonitor': 19}
voc_class_colors = {'aeroplane': [128, 0, 0], 'bicycle': [0, 128, 0], 'bird': [128, 128, 0], 'boat': [0, 0, 128], 'bottle': [128, 0, 128]
                    , 'bus': [0, 128, 128], 'car': [128, 128, 128], 'cat': [64, 0, 0], 'chair': [192, 0, 0], 'cow': [64, 128, 0]
                    , 'diningtable': [192, 128, 0], 'dog': [64, 0, 128], 'horse': [192, 0, 128], 'motorbike': [64, 128, 128], 'person': [192, 128, 128]
                    , 'pottedplant': [0, 64, 0], 'sheep': [128, 64, 0], 'sofa': [0, 192, 0], 'train': [128, 192, 0], 'tvmonitor': [0, 64, 128]
                    , 'object_class_border': [224, 224, 192]}


def rotate_img(image, angles):
    """
    Rotate image.
    @param image: image
    @param angles: angles
    @return: rotated image
    """
    image = rotate(image, angles, resize=True)
    return  image

def resize_img(image, resize_val, mask=False):
    """
    Resize image.
    @param image: image
    @return: resized image
    """
    image = cv2.resize(image, (resize_val, resize_val))
    if mask:
        return image[:,:,np.newaxis]
    else: return image
    

def count_values(dict_images):
    """
    Count values in dict_images
    @Param dict_images: dict of images
    @return: dict of values
    """
    values = []
    for key in dict_images.keys():
        values.append(len(dict_images[key]))
    
    # get max value of list of values and index
    max_value = max(values)
    index = values.index(max_value)
    return values , (max_value, index)


################################################################
#                   Data Augmentation                          #
################################################################

# Check out the segmentation data

def get_objects():
    """
    Get objects from the dataset
    @return: objects
    """
    list_objects, list_im_classes, list_im_rgb = [], [], []
    files = glob('VOCdevkit/VOC2007/SegmentationClass/*.png')
    # Read files and show the images
    for i in range(len(files)):
        file = files[i].split('/')[-1].split('.')[0]
        file = file.replace('SegmentationClass', '')
        rgb_file = 'VOCdevkit/VOC2007/JPEGImages/' + file + '.jpg'
        class_file = 'VOCdevkit/VOC2007/SegmentationClass/' + file + '.png'
        object_file = 'VOCdevkit/VOC2007/SegmentationObject/' + file + '.png'

        im_rgb = cv2.imread(rgb_file)
        im_rgb = cv2.cvtColor(im_rgb, cv2.COLOR_BGR2RGB)
        list_im_rgb.append(im_rgb)
        im_class = cv2.imread(class_file)
        im_class = cv2.cvtColor(im_class, cv2.COLOR_BGR2RGB)
        list_im_classes.append(im_class)
        im_object = cv2.imread(object_file)
        im_object = cv2.cvtColor(im_object, cv2.COLOR_BGR2RGB)
        list_objects.append(im_object)
    return list_objects, list_im_classes, list_im_rgb

def color2idx(c):
  return c[0]*256**2 + c[1]*256 + c[2]


def SegmentImagesDictionary(im_class, im_object, im_rgb):
    """
    Segment images into dictionary
    @param im_class: image class
    @param im_object: image object
    @param im_rgb: image rgb
    @return: dictionary of images
    """
    
    voc_class_indices = {}
    for k in voc_class_colors.keys():
        color = voc_class_colors[k]
        voc_class_indices[color2idx(color)] = k

    im_class = color2idx(im_class.transpose((2,0,1)))
    im_object = color2idx(im_object.transpose((2,0,1)))
    object_container = {}
    counter = 0
    curr_classes = np.unique(im_class) # the first and the last ones are background and borders respectively
    for idx in curr_classes[1:-1]:
        cls = voc_class_indices[idx]
        im_class_object = (im_class==idx).astype(np.int32) * im_object
        curr_objects = np.unique(im_class_object) # the first and the last ones are background and borders respectively
        for idx in curr_objects[1:]:
            mask_object = (im_class_object==idx).astype(np.uint8)
            pix_idx = np.where(mask_object)
            y_min, y_max, x_min, x_max = [pix_idx[0][0], pix_idx[0][-1], np.min(pix_idx[1]), np.max(pix_idx[1])]

            mask_object_crop = mask_object[y_min:y_max, x_min:x_max]
            rgb_object_crop = im_rgb[y_min:y_max, x_min:x_max]
            mask_object_crop = cv2.resize(mask_object_crop, (60, 60))
            rgb_object_crop = cv2.resize(rgb_object_crop, (60, 60))
            

            # reshape mask_object_crop to be 223 233
            object_container[counter] = {'class': cls, 'rgb': rgb_object_crop, 'mask': mask_object_crop[:,:,np.newaxis]}
            counter += 1

    return object_container

   



                    
def corrupt_image(sample, list_classes, list_im_rgb, list_im_object, rand_trans=False):
    """
    Corrupt image
    @param sample: image to corrupt
    @param list_classes: list of classes that can be used for corrupt the image
    @param list_im_rgb: list of rgb images that can be used for corrupt the images
    @param list_im_object: list of object images that can be used for corrupt the images
    @param rand_trans : if true
    """
    im = cv2.cvtColor(sample, cv2.COLOR_BGR2RGB)
    im = cv2.resize(im, (224, 224))
    H, W, _ = im.shape
    index = random.randint(0, len(list_classes)-1)
    object_container = SegmentImagesDictionary(list_classes[index], list_im_object[index], list_im_rgb[index])
    count = 0
    y_class = np.zeros(NUM_CLASSES)

    for k in object_container.keys():
        obj = object_container[k]
        y_class[voc_classes[obj['class']]] = 1.0
        if count == 3: break
        if rand_trans:
            val = random.randint(1,2)
            if val % 2 == 0:
                # apply rotation
                angles =  random.randint(0,359)
                obj['rgb'] = rotate_img(obj['rgb'], angles)
                obj['mask'] = rotate_img(obj['mask'], angles)
                
            else:
                # apply resize
                resize_val = random.randint(40,120)
                obj['rgb'] = resize_img(obj['rgb'], resize_val)
                obj['mask'] = resize_img(obj['mask'],resize_val ,mask=True)
        
        h, w, _ = obj['rgb'].shape
        #y, x = [np.random.randint(0, min(H-h), H)), np.random.randint(0, min(abs(W-w), W))]
        y, x = [np.random.randint(0, H-h), np.random.randint(0, W-w)]
        im[y:y+h, x:x+w, :] = im[y:y+h, x:x+w, :] * (1-obj['mask']) + obj['rgb'] * obj['mask']
        count += 1
    return im, y_class

# ytrain[0][0. 0. 0. 0. 0. 0. 1. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]

def preprocessing(dict_classes, list_classes, list_im_rgb, list_im_object,train_len, balanced=False, rand_trans=False):
    """
    Pre processing x_train y_train
    @param dict_classes: dictionari of classes
    @param list_classes: list of classes
    @param list_im_rgb: list of rgb of each images
    @param list_im_object: list of object of each images
    @param train_len: length of train
    @param balanced: if true, the dataset will be balanced
    @param rand_trans : if true, on data corruption will be applied random transformations
    @return: x_train, y_train
    """
    train_y = []
    count = 0
    if balanced:
        value = int(len(dict_classes["person"]) * 0.7)
    else:
        value = 500
    for key in dict_classes.keys():
        if key != "person":
            max_i = len(dict_classes[key])
            rang = value - max_i
            print("For class " , key, " we add ", rang, " values")
            for i in range(rang):
                img = io.imread("VOCdevkit/VOC2007/JPEGImages/" + dict_classes[key][i % max_i])
                img, y_class = corrupt_image(img, list_classes, list_im_rgb, list_im_object, rand_trans)
                y_class[voc_classes[key]] = 1.0
                img = cv2.resize(img, (224, 224))
                io.imsave("P1_images/Images_tr/" + str(train_len + count) + ".jpg" , img, check_contrast=False)
                train_y.append(y_class)
                count += 1
    train_y = np.array(train_y)
    print("Size of train_y is: ", len(train_y))
    print("Total Samples added are:" , count)
    return train_y