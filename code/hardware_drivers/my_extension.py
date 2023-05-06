import math

def clip(value, lower, upper):
    return lower if value < lower else upper if value > upper else value

def map(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def angle2pwm(angle):
    return angle / 18 + 2

def rotateVector(x, y, angle):
    # convert angle to radians
    angle_rad = math.radians(angle)
    
    # compute the sine and cosine of the angle
    sin_theta = math.sin(angle_rad)
    cos_theta = math.cos(angle_rad)
    
    # define the rotation matrix
    rotation_matrix = ((cos_theta, -sin_theta), (sin_theta, cos_theta))
    
    # apply the rotation matrix to the vector
    x_prime = x * rotation_matrix[0][0] + y * rotation_matrix[0][1]
    y_prime = x * rotation_matrix[1][0] + y * rotation_matrix[1][1]
    
    # return the rotated vector
    return (x_prime, y_prime)

def dist3(x1, x2, y1, y2, z1 = 0, z2 = 0):
    return math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1) + (z2 - z1) * (z2 - z1))
 