import os
import numpy as np
from skimage import io, transform

input_path = "Training_Data_p1\\ISBI2016_ISIC_Part1_Training_Data\\"
target_path = "Training_GroundTruth_p1\\ISBI2016_ISIC_Part1_Training_GroundTruth\\"
output_path_img = "Training_Data_p1_DA\\"
output_path_ground = "Training_GroundTruth_p1_DA\\"


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

def data_augmentation(input_path, target_path, output_path, output_target_path):
    for path_in, path_targ in zip(input_path, target_path):
        name = path_in.split("\\")[-1].split(".")[0]
        img = io.imread(path_in)
        target = io.imread(path_targ)
        img_90 = transform.rotate(img,90)
        target_90 = transform.rotate(target,90)
        img_180 = transform.rotate(img, 180)
        target_180 = transform.rotate(target, 180)
        io.imsave(output_path + name + "_90.jpg", img_90)
        io.imsave(output_path + name + "_180.jpg", img_180)
        io.imsave(output_target_path + name + "_90.png", target_90)
        io.imsave(output_target_path + name + "_180.png", target_180)

        

path_inp, path_targ = get_paths(input_path, target_path)
data_augmentation(path_inp, path_targ, output_path_img, output_path_ground)
