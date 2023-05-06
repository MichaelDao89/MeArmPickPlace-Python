
from turtle import *
from math import *
from PIL import Image
import os
from subprocess import call
from time import strftime, localtime

scaling = 2
gridCellSize = 25
setup(1000, 1000)
tracer(False)
bgcolor('light grey')
normalFont = ("Arial", 12 * scaling, "normal")
titleFont = ("Arial", 25 * scaling, "bold")
highlightedFont = ("Arial", 15 * scaling, "normal")

def drawGrid():
    # Draw the grid lines
    pensize(1)
    pencolor('Lavender')
    for i in range(-800* scaling, 801* scaling, gridCellSize * scaling):
        penup()
        goto(-800 * scaling, i)
        pendown()
        goto(800 * scaling, i)
    for i in range(-800* scaling, 801* scaling, gridCellSize * scaling):
        penup()
        goto(i, -800 * scaling)
        pendown()
        goto(i, 800 * scaling)


    # Draw the X-axis
    pencolor('black')
    pensize(2)
    penup()
    goto(-800 * scaling, 0)
    pendown()
    forward(1600 * scaling)

    # Draw the Y-axis
    penup()
    goto(0, -800 * scaling)
    pendown()
    setheading(90)
    forward(1600 * scaling)

    # Draw the X-axis tick marks
    for i in range(-800 * scaling, 801* scaling, 25 * scaling):
        penup()
        goto(i, -2 * scaling)
        pendown()
        goto(i, 2 * scaling)

    # Draw the Y-axis tick marks
    for i in range(-800* scaling, 801* scaling, 25 * scaling):
        penup()
        goto(-2 * scaling, i)
        pendown()
        goto(2 * scaling, i)

    penup()
    goto(-450 * scaling, -450 * scaling)
    note = 'Scale: ' + str(scaling)
    write(note, font=titleFont, align='left')
    rt(180)
    fd(35 * scaling)
    write(' Cell size: ' + str(gridCellSize), font=titleFont, align='left')

    penup()
    goto(0, 0)
    #done()

def drawMark(position, radius, name=None, labelFont = normalFont):
    penup()
    goto(position[0] * scaling, position[1] * scaling)
    pendown()
    dot(radius * scaling)
    penup()

    if name:
        penup()
        goto(position[0] * scaling + 5 * scaling, position[1] * scaling)
        pendown()
        write(name, font=labelFont)

def drawMarkLinked(posPrevious, position, radius):
    penup()
    goto(posPrevious[0] * scaling, posPrevious[1] * scaling)
    pendown()
    
    if (dist(posPrevious, position) <= radius * 10):
        pensize(2)
        pencolor('black')
    else:
        pensize(1)
        pencolor('grey')
    
    goto(position[0] * scaling, position[1] * scaling)
    dot(radius * scaling)
    penup()

def drawCircle(position, radius, name=None, labelFont = normalFont, color='black', w = 1):
    pensize(w)

    penup()
    goto(position[0] * scaling, position[1] * scaling)
    pencolor('red')
    pendown()
    dot(2 * scaling)
    penup()
    pencolor(color)

    setheading(0)
    right(90)
    forward(radius * scaling)
    left(90)
    pendown()
    circle(radius * scaling)
    if name:
        penup()
        goto(position[0] * scaling + (radius + 5) * scaling, position[1] * scaling)
        pendown()
        write(name, font=labelFont)

def extract_legacy(input_string):
    result = []
    lines = input_string.split('\n')
    for line in lines:
        if line.strip() == '':
            continue
        parts = line.split()
        angle = float(parts[1][:-1])
        dis = float(parts[3])
        result.append([angle, dis])
    result.sort(key=lambda x: x[0])
    return result

#input format: [(angle in degree, distance in mm), (angle, distance), ...)]
def extract(input):
    result = []
    for item in input:
        if item[1] > 0.1:
            result.append(item)
    result.sort(key=lambda x: x[0])
    return result

def calculatePosition(angle, dis):
    rad = radians(angle)
    x = sin(rad) * dis
    y = cos(rad) * dis

    #print('Pos: (' + str(x) + ', ' + str(y) + ')')
    return [x, y]
    
def circles_from_p1p2r(p1, p2, r):
    'Following explanation at http://mathforum.org/library/drmath/view/53027.html'
    if r == 0.0:
        return None, None
        #raise ValueError('radius of zero')
    (x1, y1), (x2, y2) = p1, p2
    if p1 == p2:
        #raise ValueError('coincident points gives infinite number of Circles')
        #print('coincident points gives infinite number of Circles: ' + str(p1) + ' ' + str(p2))
        return None, None
    # delta x, delta y between points
    dx, dy = x2 - x1, y2 - y1
    # dist between points
    q = sqrt(dx**2 + dy**2)
    if q > 2.0*r:
        #raise ValueError('separation of points > diameter')
        #print('eparation of points > diameter: ' + str(p1) + ' ' + str(p2))
        return None, None
    # halfway point
    x3, y3 = (x1+x2)/2, (y1+y2)/2
    # distance along the mirror line
    d = sqrt(r**2-(q/2)**2)
    # One answer
    c1 = (x3 - d*dy/q, y3 + d*dx/q, abs(r))
    # The other answer
    c2 = (x3 + d*dy/q, y3 - d*dx/q, abs(r))
    return c1, c2

def dist(p1, p2):
    return sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

targetRadius = 17.5
armPos = [85, 5] #using the mirrored space. Need to SWAP x and y in Arduino IDE, this is only used for drawing purpose
armRange = 170
sonarPos = [0, 0]
sonarRange = 200
latestURL = ""

def findTarget(input):
    drawGrid()
    data = extract(input)
    if (len(data) < 3): return None

    points = []
    for i in range(len(data)):
       p = calculatePosition(data[i][0] - 90, data[i][1])
       p[0] *= -1           ####### Mirrored X, compared to real physical state
       points.append(p)
       #drawMark(p, 2)
       if (i > 0):
            drawMarkLinked(points[i - 1], p, 5)
            #print(str(points[i - 1][0]))

    rootPos = sonarPos
    rootRange = sonarRange

    interval = 3
    current = interval
    candidates = []
    for i in range(len(points)):
        if (i == current):
            c = circles_from_p1p2r(points[i - 1], points[i - interval], targetRadius)
            if (c[0] is not None and c[1] is not None):
                #Choose the answer further away from us
                position = []
                if (c[1][1] > c[0][1]):
                    position = [c[1][0], c[1][1]]
                else:
                    position = [c[0][0], c[0][1]]
                candidates.append(position)
                drawCircle(position, targetRadius)
            current += interval
    
    drawCircle(rootPos, rootRange, 'sonar range', normalFont, 'blue')
    drawCircle(rootPos, 20, 'sonar', normalFont, 'blue')
    drawMark(rootPos, 5)
    sumDist = 0
    finalCandidates = []
    # Filter candidates
    for i in range(len(candidates)):
        # Only cares about ones that are in range
        d = dist(candidates[i], rootPos);
        if (d < rootRange):
            finalCandidates.append([candidates[i], d])
            sumDist += d
            drawCircle(candidates[i], targetRadius, color='green', w=1)

    targetPos = None
    # Find the one closest to the average candidate distance
    if (len(finalCandidates) > 0):
        # Find Median algorithm
        print(f"tri: Final candidates count: {len(finalCandidates)}")
        print(f"tri: Median index: {floor(len(finalCandidates) / 2)}")
        mostLikelyIndex = floor(len(finalCandidates) / 2)  
        targetPos = finalCandidates[mostLikelyIndex][0]
        drawCircle(targetPos, targetRadius, 'FINAL', highlightedFont, 'red', 3)

    # Pass it on to the arm
    drawCircle(armPos, armRange, 'arm range', normalFont, 'brown', 1)
    drawCircle(armPos, 30, 'arm', normalFont, 'brown', 2)
    drawMark(armPos, 10)

    canvas = getcanvas()
    psFilename = "turtle.ps"
    canvas.postscript(file=psFilename)
    psimage = Image.open(psFilename)
    
    imgName = 'Sonar_result_at_' + strftime("%Y-%m-%d_%H:%M:%S", localtime()) + '.jpg'

    savePath = f"webserver/static/images/scan_output/{imgName}"
    psimage.save(savePath)

    global latestURL
    latestURL = f"static/images/scan_output/{imgName}"
    print('Saved to ' + savePath)
    os.remove(psFilename)
    #done()

    reset()
    return targetPos

def getLatestURL():
    return latestURL




