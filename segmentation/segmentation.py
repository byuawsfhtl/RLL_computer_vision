############# CHANGE THESE LINES ################
modelPath = 'model/model_final.pth'
imageFolders = ['data/vol85','data/vol88','data/vol90','data/vol94']
snippetOutputPath = 'snippets/'

model:str = 'COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml'
numberOfClasses:int = 1

#################################################

from os import listdir
from os import path

for folder in imageFolders:
        assert path.exists(folder)

from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from cv2 import imread
from cv2 import imwrite
import numpy

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
        
        for boxI in range(len(numpyBoxes)):
                box = numpyBoxes[boxI]
                left = int(box[0])
                top = int(box[1])
                right = int(box[2])
                bottom = int(box[3])
                croppedImage = image[top:bottom,left:right]
                imgName = imagePath.split('/')[-1] + '-' + str(boxI) + '.jpg'
                imwrite(path.join(snippetOutputPath, imgName), croppedImage)

setup()
for imageFolder in imageFolders:
        for imageName in listdir(imageFolder):
                if '.jpg' in imageName:
                        prediction(path.join(imageFolder, imageName))
