
from turtle import *
from math import *
import os
from PIL import Image

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

def extract(input_string):
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

def calculatePosition(angle, dis):
    rad = radians(angle)
    x = sin(rad) * dis
    y = cos(rad) * dis

    #print('Pos: (' + str(x) + ', ' + str(y) + ')')
    return [x, y]
    
def circles_from_p1p2r(p1, p2, r):
    'Following explanation at http://mathforum.org/library/drmath/view/53027.html'
    if r == 0.0:
        raise ValueError('radius of zero')
    (x1, y1), (x2, y2) = p1, p2
    if p1 == p2:
        #raise ValueError('coincident points gives infinite number of Circles')
        print('coincident points gives infinite number of Circles: ' + str(p1) + ' ' + str(p2))
        return None, None
    # delta x, delta y between points
    dx, dy = x2 - x1, y2 - y1
    # dist between points
    q = sqrt(dx**2 + dy**2)
    if q > 2.0*r:
        #raise ValueError('separation of points > diameter')
        print('eparation of points > diameter: ' + str(p1) + ' ' + str(p2))
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

inLogSmall = """Angle: 20. Dis: 629.92
Angle: 25. Dis: 621.34
Angle: 30. Dis: 543.83
Angle: 35. Dis: 539.54
Angle: 40. Dis: 621.69
Angle: 45. Dis: 709.50
Angle: 50. Dis: 709.84
Angle: 55. Dis: 718.76
Angle: 85. Dis: 135.14
Angle: 90. Dis: 130.85
Angle: 95. Dis: 131.03
Angle: 100. Dis: 130.85
Angle: 105. Dis: 126.57
Angle: 110. Dis: 126.57
Angle: 115. Dis: 130.85
Angle: 120. Dis: 131.37
Angle: 125. Dis: 131.37
Angle: 130. Dis: 131.54
Angle: 135. Dis: 131.37
Angle: 140. Dis: 144.57
"""
inLogLongRangeEmpty = """Angle: 20. Dis: 372.33
Angle: 25. Dis: 380.73
Angle: 30. Dis: 376.44
Angle: 35. Dis: 376.44
Angle: 40. Dis: 674.17
Angle: 45. Dis: 723.04
Angle: 50. Dis: 745.00
Angle: 55. Dis: 763.00
Angle: 60. Dis: 849.95
Angle: 65. Dis: 875.68
Angle: 70. Dis: 884.60
Angle: 75. Dis: 1012.36
Angle: 80. Dis: 999.16
Angle: 95. Dis: 347.97
Angle: 120. Dis: 803.48
Angle: 125. Dis: 790.62
Angle: 130. Dis: 820.46
Angle: 135. Dis: 816.68
Angle: 140. Dis: 782.90
"""
inLogLongRangeWithCylinder_Right = """Angle: 10. Dis: 175.27
Angle: 12. Dis: 292.75
Angle: 14. Dis: 292.92
Angle: 16. Dis: 292.92
Angle: 18. Dis: 175.27
Angle: 20. Dis: 162.24
Angle: 22. Dis: 157.95
Angle: 24. Dis: 157.95
Angle: 26. Dis: 153.66
Angle: 28. Dis: 153.84
Angle: 30. Dis: 153.66
Angle: 32. Dis: 153.84
Angle: 34. Dis: 153.84
Angle: 36. Dis: 153.66
Angle: 38. Dis: 149.55
Angle: 40. Dis: 149.55
Angle: 42. Dis: 149.38
Angle: 44. Dis: 149.55
Angle: 46. Dis: 149.55
Angle: 48. Dis: 149.55
Angle: 50. Dis: 149.55
Angle: 52. Dis: 149.55
Angle: 54. Dis: 149.55
Angle: 56. Dis: 149.55
Angle: 58. Dis: 149.55
Angle: 60. Dis: 149.55
Angle: 62. Dis: 149.55
Angle: 64. Dis: 149.55
Angle: 66. Dis: 149.55
Angle: 68. Dis: 149.55
Angle: 70. Dis: 149.38
Angle: 72. Dis: 149.55
Angle: 74. Dis: 153.66
Angle: 76. Dis: 158.47
Angle: 78. Dis: 158.47
Angle: 80. Dis: 162.58
Angle: 82. Dis: 162.75
Angle: 84. Dis: 158.47
Angle: 86. Dis: 162.75
Angle: 88. Dis: 162.75
Angle: 90. Dis: 443.84
Angle: 92. Dis: 443.84
Angle: 94. Dis: 443.84
Angle: 96. Dis: 444.36
Angle: 98. Dis: 448.47
Angle: 100. Dis: 448.64
Angle: 102. Dis: 448.64
Angle: 104. Dis: 448.64
Angle: 106. Dis: 444.36
Angle: 108. Dis: 444.36
Angle: 110. Dis: 444.19
Angle: 112. Dis: 444.36
Angle: 114. Dis: 444.36
Angle: 116. Dis: 448.64
Angle: 118. Dis: 448.64
Angle: 120. Dis: 453.27
Angle: 122. Dis: 453.45
Angle: 124. Dis: 457.73
Angle: 126. Dis: 457.73
Angle: 128. Dis: 453.27
Angle: 130. Dis: 453.45
Angle: 132. Dis: 453.45
Angle: 134. Dis: 457.73
Angle: 136. Dis: 457.39
Angle: 138. Dis: 471.80
Angle: 140. Dis: 475.06
Angle: 142. Dis: 470.77
Angle: 144. Dis: 466.48
Angle: 146. Dis: 474.20
Angle: 148. Dis: 475.06
Angle: 150. Dis: 537.48
Angle: 152. Dis: 529.08
Angle: 154. Dis: 537.48
Angle: 156. Dis: 533.19
Angle: 158. Dis: 533.19
Angle: 160. Dis: 546.23
Angle: 162. Dis: 546.23
Angle: 164. Dis: 542.11
Angle: 166. Dis: 541.94
Angle: 168. Dis: 595.28
Angle: 170. Dis: 586.53
Angle: 172. Dis: 599.91
Angle: 174. Dis: 590.99
Angle: 176. Dis: 591.33
Angle: 178. Dis: 587.04
Angle: 180. Dis: 587.04
"""
inLogLongRangeWithCylinder_Left = """Angle: 10. Dis: 322.93
Angle: 12. Dis: 322.93
Angle: 14. Dis: 322.93
Angle: 16. Dis: 327.05
Angle: 18. Dis: 327.05
Angle: 20. Dis: 326.88
Angle: 22. Dis: 322.93
Angle: 24. Dis: 322.93
Angle: 26. Dis: 322.93
Angle: 28. Dis: 322.93
Angle: 30. Dis: 327.05
Angle: 32. Dis: 340.26
Angle: 34. Dis: 340.43
Angle: 36. Dis: 340.08
Angle: 38. Dis: 335.97
Angle: 40. Dis: 340.43
Angle: 42. Dis: 340.08
Angle: 44. Dis: 460.13
Angle: 46. Dis: 456.02
Angle: 48. Dis: 451.90
Angle: 50. Dis: 443.33
Angle: 52. Dis: 443.33
Angle: 54. Dis: 443.50
Angle: 56. Dis: 443.16
Angle: 58. Dis: 443.50
Angle: 60. Dis: 375.24
Angle: 62. Dis: 387.93
Angle: 64. Dis: 388.28
Angle: 66. Dis: 375.07
Angle: 68. Dis: 366.67
Angle: 70. Dis: 370.95
Angle: 72. Dis: 366.67
Angle: 74. Dis: 366.50
Angle: 76. Dis: 366.67
Angle: 78. Dis: 366.67
Angle: 80. Dis: 379.87
Angle: 82. Dis: 379.70
Angle: 84. Dis: 379.87
Angle: 86. Dis: 439.73
Angle: 88. Dis: 439.73
Angle: 90. Dis: 439.90
Angle: 92. Dis: 439.90
Angle: 94. Dis: 444.01
Angle: 96. Dis: 443.84
Angle: 98. Dis: 444.01
Angle: 100. Dis: 448.30
Angle: 102. Dis: 448.99
Angle: 104. Dis: 448.99
Angle: 106. Dis: 448.64
Angle: 108. Dis: 135.83
Angle: 110. Dis: 131.54
Angle: 112. Dis: 127.42
Angle: 114. Dis: 127.42
Angle: 116. Dis: 127.42
Angle: 118. Dis: 123.14
Angle: 120. Dis: 123.14
Angle: 122. Dis: 123.31
Angle: 124. Dis: 123.31
Angle: 126. Dis: 119.02
Angle: 128. Dis: 118.85
Angle: 130. Dis: 119.02
Angle: 132. Dis: 119.02
Angle: 134. Dis: 118.85
Angle: 136. Dis: 119.02
Angle: 138. Dis: 119.02
Angle: 140. Dis: 118.85
Angle: 142. Dis: 119.02
Angle: 144. Dis: 119.02
Angle: 146. Dis: 119.02
Angle: 148. Dis: 119.02
Angle: 150. Dis: 119.02
Angle: 152. Dis: 119.02
Angle: 154. Dis: 119.02
Angle: 156. Dis: 119.02
Angle: 158. Dis: 123.65
Angle: 160. Dis: 123.82
Angle: 162. Dis: 123.65
Angle: 164. Dis: 123.65
Angle: 166. Dis: 123.65
Angle: 168. Dis: 123.65
Angle: 170. Dis: 123.65
Angle: 172. Dis: 123.31
Angle: 174. Dis: 127.94
Angle: 176. Dis: 141.14
Angle: 178. Dis: 140.97
Angle: 180. Dis: 591.50
"""
inLogLongRangeWithCylinder_Center = """Angle: 10. Dis: 442.47
Angle: 12. Dis: 446.93
Angle: 14. Dis: 335.97
Angle: 16. Dis: 335.97
Angle: 18. Dis: 442.64
Angle: 20. Dis: 335.97
Angle: 22. Dis: 442.64
Angle: 24. Dis: 441.96
Angle: 26. Dis: 446.93
Angle: 28. Dis: 446.93
Angle: 30. Dis: 438.35
Angle: 32. Dis: 438.53
Angle: 34. Dis: 438.35
Angle: 36. Dis: 442.64
Angle: 38. Dis: 442.64
Angle: 40. Dis: 442.81
Angle: 42. Dis: 442.81
Angle: 44. Dis: 446.93
Angle: 46. Dis: 446.93
Angle: 48. Dis: 450.87
Angle: 50. Dis: 451.22
Angle: 52. Dis: 459.45
Angle: 54. Dis: 600.42
Angle: 56. Dis: 472.14
Angle: 58. Dis: 476.43
Angle: 60. Dis: 471.97
Angle: 62. Dis: 166.18
Angle: 64. Dis: 166.36
Angle: 66. Dis: 162.24
Angle: 68. Dis: 162.24
Angle: 70. Dis: 148.86
Angle: 72. Dis: 149.03
Angle: 74. Dis: 148.86
Angle: 76. Dis: 144.57
Angle: 78. Dis: 144.57
Angle: 80. Dis: 144.92
Angle: 82. Dis: 144.75
Angle: 84. Dis: 144.57
Angle: 86. Dis: 144.57
Angle: 88. Dis: 144.57
Angle: 90. Dis: 144.57
Angle: 92. Dis: 144.92
Angle: 94. Dis: 144.57
Angle: 96. Dis: 149.55
Angle: 98. Dis: 144.57
Angle: 100. Dis: 149.55
Angle: 102. Dis: 149.38
Angle: 104. Dis: 149.55
Angle: 106. Dis: 149.38
Angle: 108. Dis: 145.26
Angle: 110. Dis: 145.26
Angle: 112. Dis: 145.26
Angle: 114. Dis: 145.26
Angle: 116. Dis: 145.09
Angle: 118. Dis: 145.26
Angle: 120. Dis: 149.38
Angle: 122. Dis: 158.47
Angle: 124. Dis: 158.47
Angle: 126. Dis: 158.47
Angle: 128. Dis: 154.18
Angle: 130. Dis: 158.47
Angle: 132. Dis: 533.19
Angle: 134. Dis: 524.79
Angle: 136. Dis: 524.79
Angle: 138. Dis: 529.08
Angle: 140. Dis: 528.91
Angle: 142. Dis: 528.91
Angle: 144. Dis: 542.11
Angle: 146. Dis: 542.11
Angle: 148. Dis: 542.11
Angle: 150. Dis: 537.82
Angle: 152. Dis: 533.54
Angle: 154. Dis: 538.17
Angle: 156. Dis: 537.65
Angle: 158. Dis: 551.03
Angle: 160. Dis: 551.03
Angle: 162. Dis: 586.70
Angle: 164. Dis: 546.91
Angle: 166. Dis: 582.41
Angle: 168. Dis: 582.24
Angle: 170. Dis: 578.13
Angle: 172. Dis: 591.16
Angle: 174. Dis: 586.87
Angle: 176. Dis: 582.59
Angle: 178. Dis: 582.76
Angle: 180. Dis: 587.04
"""
inLogLongRangeWithCube = """Angle: 10. Dis: 318.30
Angle: 12. Dis: 318.65
Angle: 14. Dis: 318.65
Angle: 16. Dis: 322.59
Angle: 18. Dis: 318.30
Angle: 20. Dis: 318.65
Angle: 22. Dis: 318.65
Angle: 24. Dis: 322.76
Angle: 26. Dis: 335.97
Angle: 28. Dis: 335.80
Angle: 30. Dis: 438.53
Angle: 32. Dis: 438.35
Angle: 34. Dis: 438.53
Angle: 36. Dis: 438.70
Angle: 38. Dis: 438.53
Angle: 40. Dis: 442.47
Angle: 42. Dis: 442.64
Angle: 44. Dis: 442.64
Angle: 46. Dis: 446.93
Angle: 48. Dis: 451.05
Angle: 50. Dis: 413.83
Angle: 52. Dis: 413.83
Angle: 54. Dis: 418.12
Angle: 56. Dis: 147.15
Angle: 58. Dis: 147.15
Angle: 60. Dis: 147.15
Angle: 62. Dis: 133.94
Angle: 64. Dis: 129.48
Angle: 66. Dis: 129.65
Angle: 68. Dis: 129.65
Angle: 70. Dis: 129.65
Angle: 72. Dis: 129.65
Angle: 74. Dis: 125.54
Angle: 76. Dis: 125.37
Angle: 78. Dis: 125.54
Angle: 80. Dis: 125.54
Angle: 82. Dis: 125.54
Angle: 84. Dis: 125.54
Angle: 86. Dis: 121.25
Angle: 88. Dis: 121.25
Angle: 90. Dis: 120.91
Angle: 92. Dis: 120.56
Angle: 94. Dis: 120.56
Angle: 96. Dis: 120.56
Angle: 98. Dis: 120.91
Angle: 100. Dis: 120.56
Angle: 102. Dis: 120.91
Angle: 104. Dis: 121.25
Angle: 106. Dis: 120.74
Angle: 108. Dis: 117.13
Angle: 110. Dis: 117.13
Angle: 112. Dis: 117.13
Angle: 114. Dis: 116.96
Angle: 116. Dis: 117.31
Angle: 118. Dis: 116.96
Angle: 120. Dis: 116.96
Angle: 122. Dis: 117.13
Angle: 124. Dis: 116.96
Angle: 126. Dis: 117.13
Angle: 128. Dis: 117.13
Angle: 130. Dis: 117.13
Angle: 132. Dis: 117.13
Angle: 134. Dis: 117.13
Angle: 136. Dis: 117.13
Angle: 138. Dis: 117.13
Angle: 140. Dis: 121.42
Angle: 142. Dis: 121.77
Angle: 144. Dis: 121.77
Angle: 146. Dis: 121.77
Angle: 148. Dis: 121.77
Angle: 150. Dis: 121.77
Angle: 152. Dis: 121.77
Angle: 154. Dis: 122.11
Angle: 156. Dis: 121.77
Angle: 158. Dis: 121.77
Angle: 160. Dis: 127.08
Angle: 162. Dis: 130.85
Angle: 164. Dis: 131.03
Angle: 166. Dis: 130.85
Angle: 168. Dis: 130.85
Angle: 170. Dis: 130.68
Angle: 172. Dis: 144.06
Angle: 174. Dis: 144.06
Angle: 176. Dis: 259.65
Angle: 178. Dis: 255.36
Angle: 180. Dis: 255.36
"""
inLog = """Angle: 55. Dis: 393.25
Angle: 56. Dis: 372.67
Angle: 57. Dis: 362.38
Angle: 58. Dis: 367.70
Angle: 59. Dis: 359.64
Angle: 60. Dis: 365.98
Angle: 61. Dis: 381.42
Angle: 65. Dis: 389.31
Angle: 66. Dis: 379.70
Angle: 67. Dis: 365.98
Angle: 68. Dis: 361.18
Angle: 69. Dis: 360.49
Angle: 70. Dis: 355.86
Angle: 71. Dis: 363.92
Angle: 72. Dis: 139.94
Angle: 73. Dis: 139.94
Angle: 74. Dis: 139.77
Angle: 75. Dis: 139.94
Angle: 76. Dis: 139.94
Angle: 77. Dis: 135.66
Angle: 78. Dis: 135.66
Angle: 79. Dis: 135.83
Angle: 80. Dis: 135.66
Angle: 81. Dis: 135.66
Angle: 82. Dis: 135.66
Angle: 83. Dis: 135.66
Angle: 84. Dis: 135.66
Angle: 85. Dis: 135.66
Angle: 86. Dis: 131.37
Angle: 87. Dis: 131.37
Angle: 88. Dis: 131.37
Angle: 89. Dis: 131.54
Angle: 90. Dis: 131.37
Angle: 91. Dis: 131.37
Angle: 92. Dis: 131.37
Angle: 93. Dis: 131.54
Angle: 94. Dis: 131.54
Angle: 95. Dis: 127.42
Angle: 96. Dis: 127.42
Angle: 97. Dis: 127.08
Angle: 98. Dis: 127.25
Angle: 99. Dis: 127.08
Angle: 100. Dis: 127.42
Angle: 101. Dis: 127.25
Angle: 102. Dis: 127.42
Angle: 103. Dis: 127.42
Angle: 104. Dis: 127.08
Angle: 105. Dis: 127.08
Angle: 106. Dis: 127.42
Angle: 107. Dis: 127.42
Angle: 108. Dis: 127.42
Angle: 109. Dis: 127.42
Angle: 110. Dis: 127.42
Angle: 111. Dis: 127.42
Angle: 112. Dis: 127.42
Angle: 113. Dis: 127.42
Angle: 114. Dis: 127.08
Angle: 115. Dis: 127.42
Angle: 116. Dis: 136.34
Angle: 117. Dis: 136.17
Angle: 118. Dis: 136.34
Angle: 119. Dis: 136.34
Angle: 120. Dis: 136.34
Angle: 121. Dis: 136.17
Angle: 122. Dis: 136.17
Angle: 123. Dis: 136.34
Angle: 124. Dis: 136.34
Angle: 125. Dis: 136.17
Angle: 126. Dis: 132.06
Angle: 127. Dis: 132.06
Angle: 128. Dis: 132.23
Angle: 129. Dis: 132.06
Angle: 130. Dis: 132.06
Angle: 131. Dis: 136.34
Angle: 132. Dis: 136.17
Angle: 133. Dis: 136.34
Angle: 134. Dis: 149.38
Angle: 135. Dis: 153.66
Angle: 136. Dis: 153.66
Angle: 133. Dis: 149.55
Angle: 132. Dis: 136.34
Angle: 131. Dis: 136.34
Angle: 130. Dis: 136.34
Angle: 129. Dis: 136.34
Angle: 128. Dis: 136.34
Angle: 127. Dis: 136.34
Angle: 126. Dis: 136.34
Angle: 53. Dis: 353.98
Angle: 52. Dis: 353.80
Angle: 51. Dis: 353.98
Angle: 50. Dis: 353.80
Angle: 49. Dis: 358.09
Angle: 48. Dis: 371.30
Angle: 47. Dis: 371.30
Angle: 46. Dis: 371.30
Angle: 45. Dis: 367.01
Angle: 44. Dis: 367.01
Angle: 43. Dis: 371.30
Angle: 42. Dis: 371.30
Angle: 41. Dis: 371.30
Angle: 40. Dis: 384.50
Angle: 39. Dis: 702.12
Angle: 38. Dis: 702.12
Angle: 37. Dis: 706.41
Angle: 36. Dis: 693.20
Angle: 35. Dis: 697.49
Angle: 34. Dis: 697.66
Angle: 33. Dis: 697.66
Angle: 32. Dis: 640.21
Angle: 31. Dis: 653.07
Angle: 30. Dis: 653.24
Angle: 29. Dis: 635.75
Angle: 28. Dis: 653.07
Angle: 27. Dis: 635.92
Angle: 26. Dis: 640.04
Angle: 25. Dis: 640.04
Angle: 24. Dis: 635.58
Angle: 23. Dis: 639.70
Angle: 22. Dis: 626.66
Angle: 21. Dis: 626.49
Angle: 20. Dis: 626.66
Angle: 21. Dis: 626.66
Angle: 22. Dis: 626.66
Angle: 23. Dis: 630.95
Angle: 24. Dis: 630.95
Angle: 25. Dis: 626.66
Angle: 26. Dis: 631.12
Angle: 27. Dis: 626.66
Angle: 28. Dis: 640.21
Angle: 29. Dis: 640.21
"""

targetRadius = 17.5
armPos = [85, 5] #using the mirrored space. Need to flip x, y in Arduino IDE
armRange = 170
sonarPos = [0, 0]
sonarRange = 180

if __name__ == '__main__':
    drawGrid()
    #pos1 = calculatePosition(100.0-90, 110.1)
    #pos2 = calculatePosition(58.0-90,110.4)
    #drawCircle(pos1, 17.5, "1")
    #drawCircle(pos2, 17.5, "2")
    
    #data = extract(inLogLongRangeWithCylinder_Left)
    data = extract(inLogLongRangeWithCylinder_Center)
    #data = extract(inLogLongRangeWithCylinder_Right)
    points = []
    for i in range(len(data)):
       p = calculatePosition(data[i][0] - 90, data[i][1])
       p[0] *= -1           ####### Mirrored, compared to real physical state
       points.append(p)
       #drawMark(p, 2)
       if (i > 0):
            drawMarkLinked(points[i - 1], p, 5)
            #print(str(points[i - 1][0]))

    rootPos = sonarPos
    rootRange = sonarRange

    interval = 2
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

    # Find the one closest to the average candidate distance
    if (len(finalCandidates) > 0):
        #avgDist = sumDist / len(finalCandidates)
        #minDist = 10000
        mostLikelyIndex = 0

        # Find closest to Average algorithm
        #for i in range(len(finalCandidates)):
        #    if (abs(finalCandidates[i][1] - avgDist) < minDist):
        #        minDist = finalCandidates[i][1]
        #        mostLikelyIndex = i

        # Find Max algorithm
        #maxDist = 0
        #for i in range(len(finalCandidates)):
        #    if (finalCandidates[i][1] >= maxDist):
        #        maxDist = finalCandidates[i][1]
        #        mostLikelyIndex = i
        #print('max dist: ' + str(maxDist))

        # Find Median algorithm
        mostLikelyIndex = floor(len(finalCandidates) / 2)  

        drawCircle(finalCandidates[mostLikelyIndex][0], targetRadius, 'FINAL', highlightedFont, 'red', 3)

    # Pass it on to the arm
    drawCircle(armPos, armRange, 'arm range', normalFont, 'brown', 1)
    drawCircle(armPos, 30, 'arm', normalFont, 'brown', 2)
    drawMark(armPos, 10)

    ## Save the canvas
    ## get the current directory of the Python script
    #path = os.getcwd()

    ## set the file name
    #file_name = "my_turtle_image.png"

    ## combine the path and file name
    #file_path = os.path.join(path, file_name)

    ## save the turtle graphic as an image
    #getcanvas().postscript(file=file_path)
    #img = Image.open(file_path)
    #img.save(file_path[:-3] + "png", "png")
    done()



