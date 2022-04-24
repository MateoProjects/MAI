import cv2
import numpy as np
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from glob import glob



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
files = glob('VOCdevkit/VOC2007/JPEGImages/*.jpg')

n_samples = len(files)
files = files[:n_samples]

np.random.seed(0)
ridx = np.random.randint(0, n_samples, int(n_samples*0.2))
train_test_split = np.zeros(n_samples)
train_test_split[ridx] = 1


def read_files():
    """
    Reads the files in the folder and returns the list of files and the list of labels
    @return Tuple with (x_train, y_train, x_test, y_test, id_names_train, id_names_test), and 
        a dictionari images_dict
    """
    # read train and test files
    train_files = open('voc_train.txt', 'r').read().splitlines()
    test_files = open('voc_test.txt', 'r').read().splitlines()
    x_train, y_train, x_test, y_test = [], [], [], []
    id_names_train , y_train_val , id_names_test, y_test_val = [], [], [], []
    print("##### READING CONTENT #####")
    images_dict = {'aeroplane': [], 'bicycle': [], 'bird':[], 'boat': [], 'bottle': [], 'bus': [], 'car': [], 'cat': [], 'chair': [], 'cow': [], 'diningtable': [], 'dog': [], 'horse': [], 'motorbike': [], 'person': [], 'pottedplant': [], 'sheep': [], 'sofa': [], 'train': [], 'tvmonitor': []}
    for f, i in zip(files, range(n_samples)):
        name = f.split("\\")[-1]
        # name = f.split("/")[-1] # for linux
        name_file = name.replace(".jpg", "")
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
        if name_file in test_files:
            x_test.append(img)
            id_names_test.append(name)

        else:
            x_train.append(img)
            id_names_train.append(name)

        classes = np.zeros(num_classes)
        root, name = f.split('JPEGImages', 1)
        cnames, _ , info_image = read_content(root+'Annotations'+name[:-3]+'xml')
        images_dict[info_image[0]].append(info_image[1])
        for c in cnames:
            classes[c] = 1.0
                
        if name_file in test_files:
            y_test.append(classes)
        else:
            y_train.append(classes)
    
    print("##### END READING CONTENT #####")   
    print("Longitud de x_train:" , len(x_train))
    print("Longitud de x_test:" , len(x_test))
    x_train = np.array(x_train).astype(np.uint8)
    y_train = np.array(y_train)
    x_test = np.array(x_test)
    y_test = np.array(y_test)
    return (x_train, y_train, x_test, y_test, id_names_train, id_names_test), images_dict


def read_content(xml_file):
  """
  Reads the content of the xml file
  @param xml_file: path to the xml file
  @return: list of classes and the image name
  """
  tree = ET.parse(xml_file)
  root = tree.getroot()
  
  list_with_all_boxes = []
  list_with_all_objects = []
  name_file = root.find("filename").text

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

  return list_with_all_objects, list_with_all_boxes , (classname, name_file)


def plot_balance_data(y_train, balance=False):
    """
    Plots the balance data of the train set
    @param y_train: labels of the train set
    @param balance: if True, the data is balanced
    """
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    labs = voc_classes.keys()
    data_balance = np.sum(y_train, 0) / y_train.shape[0]
    ax.bar(labs,data_balance)
    ax.set_title('Balance de datos')
    print(data_balance)
    plt.xticks([i for i in range(20)], labs, rotation='vertical')
    if balance:
        plt.savefig('balance_data.png')
    else:
        plt.savefig('no_balance_data.png')
    plt.close()