modelPath = 'model/rowSegment/model_final.pth'
imageFolders = ['data/' + i for i in ['vol85','vol88','vol90','vol94'] ]
snippetOutputPath = 'snippets/row/'

import json
from base64 import b64encode
from os import listdir
from os import path

for folder in imageFolders:
        assert path.exists(folder)

from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from cv2 import imread
from cv2 import imwrite
from cv2 import imencode
import numpy

model:str = 'COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml'
numberOfClasses:int = 1

def makeShape(points:[int,int]) -> dict:
        shape = dict()
        shape['label'] = 'row'
        left = float(points[0])
        top = float(points[1])
        right = float(points[2])
        bottom = float(points[3])
        shape['points'] = [[left,top],[right,top],[right,bottom],[left,bottom]]
        shape['group_id'] = None
        shape['shape_type'] = 'polygon'
        shape['flags'] = {}
        return shape

def makeShapes(pointsList:[list]) -> [dict]:
        return [makeShape(points) for points in pointsList]

def toLabelme(image, imagePath, points:[list]):
        '''Save the prediction as a labelme json'''
        labelme = dict()
        labelme['version'] = '4.6.0'
        labelme['flags'] = {}
        labelme['shapes'] = makeShapes(points)
        labelme['imagePath'] = imagePath
        jpgImg = imencode('.jpg', image)
        labelme['imageData'] = b64encode(jpgImg[1]).decode('utf-8')
        height, width = image.shape[:2]
        labelme['imageHeight'] = height
        labelme['imageWidth'] = width
        return labelme

predictor = None
def setup():
        global predictor
        cfg = get_cfg()
        cfg.merge_from_file(model_zoo.get_config_file(model))
        # cfg.MODEL.DEVICE = 'cpu'
        cfg.MODEL.ROI_HEADS.NUM_CLASSES = numberOfClasses
        cfg.MODEL.WEIGHTS = modelPath
        predictor = DefaultPredictor(cfg)

def prediction(imagePath):
        image = imread(imagePath)
        if image is None:
                print(imagePath)
                return
        outputs = predictor(image)
        objects = outputs['instances'].pred_classes
        boxes = outputs['instances'].pred_boxes
        numpyObjects = objects.cpu().numpy()
        numpyBoxes = boxes.tensor.cpu().numpy()
        labelmeJson = toLabelme(image, imagePath, [list(i) for i in numpyBoxes])
        justImName = imagePath.split('/')[-1]
        json.dump(labelmeJson, open(snippetOutputPath + justImName + '.json', 'w'))

setup()
for imageFolder in imageFolders:
        for imageName in listdir(imageFolder):
                if '.jpg' in imageName:
                        prediction(path.join(imageFolder, imageName))
