PAGE_BREAK_THRESH = 200
CONNECTED_THRESH = 10

VOLUME_NUM = '88'
IMAGE_NUM = '70'

import os
import json

jsonName = 'record_image_vol_' + VOLUME_NUM + '_num_' + IMAGE_NUM + '.json'

os.chdir(r'V:\FHSS-JoePriceResearch\papers\current\colorado_land_patents\data\tract books\row from full training')
j = json.load(open(jsonName,'r'))
shapes = j['shapes']

'''              ===labelme points===
order placed

-x-
low -> high

-y-
low  |
high V
'''


'''              ===user instructions===

place the points in the following order: 
3 2 
0 1 

joins then happen between shape[i] and shape[i+1]
 an exception when shape[i] is bottom of page 1 and shape[i+1] is top of page 2 
'''

def pageBreak(a:[list], b:[list]) -> bool:
    return abs(a[0][1] - b[3][1]) > PAGE_BREAK_THRESH

def connected(a:[list], b:[list]) -> bool:
    return abs(a[0][0] - b[3][0]) <= CONNECTED_THRESH and abs(a[0][1] - b[3][1]) <= CONNECTED_THRESH

def connect(a:dict, b:dict) -> dict:
    global shapesAdded
    a = a['points']
    b = b['points']
    if pageBreak(a,b):
        return False
    if connected(a,b):
        return False
    shapesAdded += 1
    return pointsToShape([b[3],b[2],a[1],a[0]])

def pointsToShape(points:[list]) -> dict:
    return {'label': 'row', 'points': points, 'group_id': None, 'shape_type': 'polygon', 'flags': {}}

def postProcess(shapes:[dict]) -> [dict]:
    out = []
    for i in shapes:
        if i is not False:
            out.append(i)
    return out

shapesAdded = 0

newShapes = list()
for i in range(len(shapes) - 1):
    newShapes.append(shapes[i])
    newShapes.append(connect(shapes[i], shapes[i+1]))
    
newShapes.append(shapes[-1])
j['shapes'] = postProcess(newShapes) 
json.dump(j, open(jsonName,'w'))
print(shapesAdded, 'shapes added')
