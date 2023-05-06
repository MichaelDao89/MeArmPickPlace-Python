from math import sqrt
from turtle import *
from PIL import Image
import os
from time import strftime, localtime

scaling = 1
gridCellSize = 10
setup(600, 600)
tracer(False)
bgcolor('light grey')
normalFont = ("Arial", 12 * scaling, "normal")
titleFont = ("Arial", 25 * scaling, "bold")
highlightedFont = ("Arial", 15 * scaling, "normal")

def drawGrid():
    print('drawing grid')
    # Draw the grid lines
    pensize(1)
    pencolor('Lavender')
    for i in range(-600* scaling, 601* scaling, gridCellSize * scaling):
        penup()
        goto(-600 * scaling, i)
        pendown()
        goto(600 * scaling, i)
    for i in range(-600* scaling, 601* scaling, gridCellSize * scaling):
        penup()
        goto(i, -600 * scaling)
        pendown()
        goto(i, 600 * scaling)


    # Draw the X-axis
    pencolor('black')
    pensize(2)
    penup()
    goto(-600 * scaling, 0)
    pendown()
    forward(1600 * scaling)

    # Draw the Y-axis
    penup()
    goto(0, -600 * scaling)
    pendown()
    setheading(90)
    forward(1600 * scaling)

    # Draw the X-axis tick marks
    for i in range(-600 * scaling, 601* scaling, 25 * scaling):
        penup()
        goto(i, -2 * scaling)
        pendown()
        goto(i, 2 * scaling)

    # Draw the Y-axis tick marks
    for i in range(-600* scaling, 601* scaling, 25 * scaling):
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

def save_canvas():
    canvas = getcanvas()
    psFilename = "turtle.ps"
    canvas.postscript(file=psFilename)
    psimage = Image.open(psFilename)
    
    imgName = 'Sonar_result_at_' + strftime("%Y-%m-%d_%H:%M:%S", localtime()) + '.jpg'

    savePath = f"webserver/static/images/scan_output/{imgName}"
    psimage.save(savePath)

    latestURL = f"static/images/scan_output/{imgName}"
    print('Saved turtle canvas to ' + savePath)
    os.remove(psFilename)

    return latestURL

def reset_canvas():
    reset()

def dist(p1, p2):
    return sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
