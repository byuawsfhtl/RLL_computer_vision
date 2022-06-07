"""project_segment.py
Segmenting and croping a dataset by one class
Also returns the bounding boxes of the segmented images

Modification of Detectron 2 Tutorial
and Sophia Rowling's Brazil Google Colab code
Logan Sowards: Computer Vision Team
"""
from sys import argv

script, img_dir= argv #This code assumes you are using the method in which the images have been split into 1000 smaller subdirectories

# Some basic setup:
# Setup detectron2 logger
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import os, json, cv2, random, torch, torchvision
import csv

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.structures import BoxMode
from detectron2.evaluation import COCOEvaluator, inference_on_dataset
from detectron2.data import build_detection_test_loader

cfg = get_cfg()

# add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.8  # set threshold for this model, I'd probably want .8
cfg.MODEL.WEIGHTS = "./final_weights.pth" # Change to weights you developed
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1 # Only one in this example, but can be changed to more
predictor = DefaultPredictor(cfg)


# Segment and separate the images you have
images = os.listdir(f"./imgs/{img_dir}/") #Change to the folder of images you want to segment

#creates a csv that will record the bounding boxes
import csv
with open(f'./bounding_boxes/bounding_box.csv', 'a') as output: #you can change bounding_box.csv to whatever name you feel is appropriate

    writer = csv.writer(output, delimiter=',')

    for im in images:
        if im[-4:] == 'json':
          continue

        image_path = f"./imgs/{img_dir}/" + im #change to directory of images you want to segment

        image_array = cv2.imread(image_path)
        print(image_path)
        outputs = predictor(image_array)
        name = outputs["instances"].pred_classes
        classes = outputs["instances"].pred_boxes

        rows = classes.tensor.cpu().numpy()

        #0=box
        row_name = name.cpu().numpy()

        print(im)
        print(row_name)

        j = 0
        i = 0

        bounding_box = [im]

        for row in rows:
          left = int(row[0])
          top = int(row[1])
          right = int(row[2])
          bottom = int(row[3])
          cropped_array = image_array[top:bottom,left:right]

          if row_name[j] == 0:
            if i == 0:
              i += 1
              cv2.imwrite(f"./imgs/segmented/snippets/{img_dir}/"+ im[:-4] + '_yourclass1.jpg', cropped_array) #change yourclass here and in the lines below
              bounding_box.append(row)
            elif i == 1:
              i += 1
              cv2.imwrite(f"./imgs/segmented/snippets/{img_dir}/"+ im[:-4] + '_yourclass2.jpg', cropped_array)
              bounding_box.append(row)
            elif i == 2:
              i += 1
              cv2.imwrite(f"./imgs/segmented/snippets/{img_dir}/"+ im[:-4] + '_yourclass3.jpg', cropped_array)
              bounding_box.append(row)
            elif i == 3:
              i += 1
              cv2.imwrite(f"./imgs/segmented/snippets/{img_dir}/"+ im[:-4] + '_yourclass4.jpg', cropped_array)
              bounding_box.append(row)
            elif i == 4:
              i += 1
              cv2.imwrite(f"./imgs/segmented/snippets/{img_dir}/"+ im[:-4] + '_yourclass5.jpg', cropped_array)
              bounding_box.append(row)
            elif i == 5:
              i += 1
              cv2.imwrite(f"./imgs/segmented/snippets/{img_dir}/"+ im[:-4] + '_yourclass6.jpg', cropped_array)
              bounding_box.append(row)
            elif i == 6:
              cv2.imwrite(f"./imgs/segmented/snippets/{img_dir}/"+ im[:-4] + '_yourclass7.jpg', cropped_array)
              bounding_box.append(row)

          j += 1
        writer.writerow(bounding_box)
