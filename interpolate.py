PAGE_BREAK_THRESH = 200
CONNECTED_THRESH = 10
APPROX_THRESH = 10
ROW_LENGTH = 1000

VOLUME_NUM = '85'
IMAGE_NUM = '11'

import os
import json



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

shapesAdded = 0

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

def addShapes():
    jsonName = 'record_image_vol_' + VOLUME_NUM + '_num_' + IMAGE_NUM + '.json'

    os.chdir(r'V:\FHSS-JoePriceResearch\papers\current\colorado_land_patents\data\tract books\row from full training')
    j = json.load(open(jsonName,'r'))
    shapes = j['shapes']
    sortedShapes = list()
    for shape in shapes:
        points = shape['points']
        newShape = pointsToShape(sortPoints(points))
        sortedShapes.append(newShape)
    shapes = sortedShapes
    
    newShapes = list()
    for i in range(len(shapes) - 1):
        newShapes.append(shapes[i])
        newShapes.append(connect(shapes[i], shapes[i+1]))
        
    newShapes.append(shapes[-1])
    j['shapes'] = postProcess(newShapes) 
    json.dump(j, open(jsonName,'w'))
    print(shapesAdded, 'shapes added')


def approx(a:float, b:float)->bool:
    return abs(a-b) < APPROX_THRESH

def rowLength(a:float, b:float)->bool:
    return abs(a-b) > ROW_LENGTH

def makeLine(a:[int,int], b:[int,int])->str:
    if(approx(a[0], b[0]) and not rowLength(a[0],b[0])):
        if(a[1] < b[1]):
            return 'Down'
        return 'Up'
    if(approx(a[1], b[1])):
        if(a[0] < b[0]):
            return 'Right'
        return 'Left'
    if(a[0] < b[0]):
        if(a[1] < b[1]):
            return 'Positive'
        return 'Negative'
    if(a[1] < b[1]):
        return 'Negative'
    return 'Positive'

def makePattern(points:[list])->[str,str]:
    return [makeLine(points[0], points[1]), makeLine(points[0], points[2])]

def matchPattern(pattern:[str,str], points:[int,int]) -> list:
    print(pattern)
    options = {'Up'    : {'Negative':[1,4,3,2], 'Positive':[2,3,4,1]},
               'Right' : {'Positive':[4,3,2,1], 'Negative':[1,2,3,4]},
               'Down'  : {'Negative':[3,2,1,4], 'Positive':[4,1,2,3]},
               'Left'  : {'Positive':[2,1,4,3], 'Negative':[3,4,1,2]}
               }
    order = options[pattern[0]][pattern[1]]
    return [[points[i], order[i]] for i in range(4)]

def sortPoints(points:[list])->[list]:
    print(points)
    newPoints = matchPattern(makePattern(points), points)
    newPoints.sort(key = lambda i : i[1])
    return [i[0] for i in newPoints]



addShapes()


