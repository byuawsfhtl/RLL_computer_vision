PAGE_BREAK_THRESH = 200
CONNECTED_THRESH = 10
APPROX_THRESH = 10
ROW_LENGTH = 1000

X_GROUPING = 900

VOLUME_NUM = '90'
IMAGE_NUM = '1'

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
joins then happen between shape[i] and shape[i+1]
 an exception when shape[i] is bottom of page 1 and shape[i+1] is top of page 2 
'''

shapesAdded = 0

def loadFile(fileName:str, workingDir:str) -> dict:
    os.chdir(workingDir)
    return json.load(open(fileName,'r'))

def saveFile(fileName:str, data):
    json.dump(data, open(fileName, 'w'))

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

def removeFalse(shapes:[dict]) -> [dict]:
    out = []
    for i in shapes:
        if i is not False:
            out.append(i)
    return out

def addShapes(jsonName:str, workingDir:str = r'V:\FHSS-JoePriceResearch\papers\current\colorado_land_patents\data\tract books\row from full training'):
    '''Interpolates between shapes; if a user annotated every other, this fills in the missing shapes'''
    j = loadFile(jsonName, workingDir)
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
    j['shapes'] = removeFalse(newShapes)
    saveFile(jsonName, j)
    print(shapesAdded, 'shapes added')
    print(VOLUME_NUM, IMAGE_NUM)


def score(points:[[int,int]]) -> [[[int,int],int]]:
    # find the left most point; find the next leftmost point; compare y values to determine which is top left and bottom left
    # leftmost
    minX:int = points[0][0]
    minXI:int = 0
    for i in range(len(points[1:])):
        if points[i][0] < minX:
            minX = points[i][0]
            minXI = i
    # next leftmost
    nextMinXI:int = 0 if minXI != 0 else 1
    nextMinX:int = points[nextMinXI][0]
    for i in range(len(points)):
        if i != minXI and points[i][0] < nextMinX:
            nextMinXI = i
            nextMinX = points[i][0]
    topI = minXI if points[minXI][1] > points[nextMinXI][1] else nextMinXI
    bottomI = nextMinXI if topI == minXI else minXI
    sign:int = bottomI- topI  # +-1
    return [[points[i], (sign)*(topI - i) % len(points)] for i in range(len(points))]
    

def sortPoints(points:[list])->[list]:
    newPoints = score(points)
    newPoints.sort(key = lambda i : i[1])
    return [i[0] for i in newPoints]


def checkShapes(workingDir:str = r'V:\FHSS-JoePriceResearch\papers\current\colorado_land_patents\data\tract books\row from full training'):
    '''Moves thru the folder and outputs image names with bad polygons
    A polygon is bad if there are not exactly 4 points'''
    os.chdir(workingDir)
    for f in os.listdir():
        if f[-len('.json'):].upper() == '.JSON':
            j = json.load(open(f,'r'))
            errors = 0
            for i in range(len(j['shapes'])):
                shape = j['shapes'][i]
                if len(shape['points']) != 4:
                    errors += 1
                    print(' ',i)
            if errors > 0:
                print(f, errors)
            
def rectToPoly(j:dict) -> dict:
    '''Changes rectangles (model output) to polygons (easier to adjust for training)'''
    shapes:[dict] = j['shapes']
    for i in range(len(shapes)):
        shape:dict = shapes[i]
        if shape['shape_type'] != 'rectangle':
            continue
        points:[list] = shape['points']
        bottom:float = points[0][1]
        left:float = points[0][0]
        top:float = points[1][1]
        right:float = points[1][0]
        newPoints:[list] = [[left,top],[right,top],[right,bottom],[left,bottom]]
        shapes[i]['points'] = newPoints
        shapes[i]['shape_type'] = 'polygon'
    j['shapes'] = shapes
    return j

def order(shapes:[dict]) -> [dict]:
    # list comprehension allows for 'x+1 where x = 0' style expressions 
    # this function order points first by x (broken into large chunks, splitting the pages)
    #  it then sorts by y value (lower y value is higher on the page) 
    key = lambda shape : [[int(mid[0] / X_GROUPING), mid[1]] for mid in [center(points) for points in [shape['points']]]][0]
    shapes.sort(key = key)
    return shapes

def center(points:[[float,float]]) -> [float,float]:
    x = sum([i[0] for i in points]) / len(points)
    y = sum([i[1] for i in points]) / len(points)
    return [x,y]

def orderFile(j:dict) -> dict:
    '''Sorts the shapes from top to bottom, left page then right page'''
    j['shapes'] = order(j['shapes'])
    return j

def smooth(j:dict, smoothFactor:float = 1.00) -> dict:
    '''Moves the right/left sides for each box towards to average for that page
    Assumes sorted polygons
    Ensures leftmost and rightmost lines are the same'''
    shapes:[dict] = j['shapes']
    # find the page break
    # for each page
    #  find the average left and right x values
    #  x = avg for each on page for side in [l,r]
    lastLeft:int = None
    for i in range(len(shapes) - 1):
        if abs(center(shapes[i]['points'])[0] - center(shapes[i+1]['points'])[0]) > 1000:
            # the next shape is on the next page
            lastLeft = i
            break

    for page in [range(lastLeft+1), range(lastLeft+1, len(shapes))]:
        avgLeft:float = 0
        avgRight:float = 0
        for i in page:
            shape = shapes[i]
            avgLeft += shape['points'][0][0]
            avgRight += shape['points'][1][0]
        avgLeft /= lastLeft
        avgRight /= lastLeft

        for i in page:
            shape = shapes[i]
            points = shape['points']
            left = points[0][0]
            leftBump = (avgLeft - left) * smoothFactor
            points[0][0] += leftBump
            points[3][0] += leftBump

            right = points[1][0]
            rightBump = (avgRight - right) * smoothFactor
            points[1][0] += rightBump
            points[2][0] += rightBump
            shape['points'] = points
            shapes[i] = shape

    j['shapes'] = shapes
    return j

jsonName = 'record_image_vol_' + VOLUME_NUM + '_num_' + IMAGE_NUM + '.jpg.json'
workingDir = r'V:\FHSS-JoePriceResearch\papers\current\colorado_land_patents\data\tract books\predicted'
j = loadFile(jsonName, workingDir)
old = j.copy()
for f in [rectToPoly, orderFile, lambda x: smooth(x, 1)]:
    new = f(old)
    old = new.copy()
saveFile(jsonName, old)

