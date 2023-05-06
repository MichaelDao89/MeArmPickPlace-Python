
from math import *
import processors.visualisation as vis

targetRadius = 17.5
armPos = [85, 5] #using the mirrored space. Need to SWAP x and y in Arduino IDE, this is only used for drawing purpose
armRange = 170
sonarPos = [0, 0]
sonarRange = 200
latestURL = ""

def findTarget(input):
    vis.drawGrid()
    data = extract(input)
    if (len(data) < 3): return None

    points = []
    for i in range(len(data)):
       p = calculatePosition(data[i][0] - 90, data[i][1])
       p[0] *= -1           ####### Mirrored X, compared to real physical state
       points.append(p)
       if (i > 0):
            vis.drawMarkLinked(points[i - 1], p, 5)
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
                vis.drawCircle(position, targetRadius)
            current += interval
    
    vis.drawCircle(rootPos, rootRange, 'sonar range', vis.normalFont, 'blue')
    vis.drawCircle(rootPos, 20, 'sonar', vis.normalFont, 'blue')
    vis.drawMark(rootPos, 5)
    sumDist = 0
    finalCandidates = []
    # Filter candidates
    for i in range(len(candidates)):
        # Only cares about ones that are in range
        d = dist(candidates[i], rootPos);
        if (d < rootRange):
            finalCandidates.append([candidates[i], d])
            sumDist += d
            vis.drawCircle(candidates[i], targetRadius, color='green', w=1)

    targetPos = None
    # Find the one closest to the average candidate distance
    if (len(finalCandidates) > 0):
        # Find Median algorithm
        print(f"tri: Final candidates count: {len(finalCandidates)}")
        print(f"tri: Median index: {floor(len(finalCandidates) / 2)}")
        mostLikelyIndex = floor(len(finalCandidates) / 2)  
        targetPos = finalCandidates[mostLikelyIndex][0]
        vis.drawCircle(targetPos, targetRadius, 'FINAL', vis.highlightedFont, 'red', 3)

    # Draw the arm 
    vis.drawCircle(armPos, armRange, 'arm range', vis.normalFont, 'brown', 1)
    vis.drawCircle(armPos, 30, 'arm', vis.normalFont, 'brown', 2)
    vis.drawMark(armPos, 10)

    global latestURL
    latestURL = vis.save_canvas()
    vis.reset_canvas()

    return targetPos

def getLatestURL():
    return latestURL

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



