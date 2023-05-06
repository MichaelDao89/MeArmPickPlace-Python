# ARM mapping
# (BCM num:) 8 - Base (Board num: 24)
# 25 - Shoulder (22)
# 24 - Elbow (18)
# 23 - Gripper (16)

from math import acos, atan, atan2, sqrt
import pigpio
from time import sleep
from my_servo import Servo
import my_extension as ext

############## CONSTANTS ##############
# You can work in any units, as long as they all match; these
# will dictate the units of the 3D space you're in.  I used millimetres.
SEGMENT_LENGTH = 80; # e.g., shoulder to elbow length
# X: avoid points inside the base, this moves X = 0 to the edge of the meArm base
# Y: use this to adjust sideway offsets
# Z: account for base to shoulder joint offset, this moves Z = 0 to the floor level of the meArm base
BASE_OFFSET = (0, 0, -50); 
STEP_SIZE = 1.0; # movement delta when lerping, in mm, lower value = higher step fidelity
SPEED = 30.0; # movement speed, in cm/seconds
ACTIONS_DELAY = 50.0; # delay between actions, in milliseconds

# Default angles
HOME_POS = [50.0, 0.0, 75.0]
GRIP_OPEN_ANGLE = 90;
GRIP_CLOSE_ANGLE = 140;

############### RUNTIME ###############
_baseServo, _shoulderServo, _elbowServo, _gripperServo = None, None, None, None
_currentPosition, _currentGrip = None, None
_stepInterval = None

def begin(pwm, basePin, shoulderPin, elbowPin, gripperPin):
    # will change these values
    global _baseServo, _shoulderServo, _elbowServo, _gripperServo
    global _stepInterval

    # Attach the servos
    if (_baseServo is None):
        pwm.set_mode(basePin, pigpio.OUTPUT)
        pwm.set_PWM_frequency(basePin, 50)
        _baseServo = Servo(basePin, pwm, 600, 2400, 0, 180)
        #_baseServo = Servo(basePin, 0, 0.750/1000, 2.250/1000)
    if (_shoulderServo is None):
        pwm.set_mode(shoulderPin, pigpio.OUTPUT)
        pwm.set_PWM_frequency(shoulderPin, 50)
        _shoulderServo = Servo(shoulderPin, pwm, 900, 2100, 0, 180)
        #_shoulderServo = Servo(shoulderPin, 0, 0.9/1000, 2.100/1000)
    if (_elbowServo is None):
        pwm.set_mode(elbowPin, pigpio.OUTPUT)
        pwm.set_PWM_frequency(elbowPin, 50)
        _elbowServo = Servo(elbowPin, pwm, 750, 2250, 0, 180)
        #_elbowServo = Servo(elbowPin, 0, 0.750/1000, 2.250/1000)
    if (_gripperServo is None):
        pwm.set_mode(gripperPin, pigpio.OUTPUT)
        pwm.set_PWM_frequency(gripperPin, 50)
        _gripperServo = Servo(gripperPin, pwm, 700, 2500, 0, 180)
        #_gripperServo = Servo(gripperPin, 0, 0.460/1000, 2.400/1000)
    print('---------------- ARM BEGIN ----------------')
    print('Servos attached')

    # Calculate dynamic constants
    _stepInterval = (STEP_SIZE / (SPEED * 0.01)) / 1000
    #_stepInterval = 50 / 1000
    print('Step interval: ' + str(_stepInterval * 1000) + ' milliseconds')

    gotoHome(True)
    openGripper()
    sleep(500 /1000)
    closeGripper()
    sleep(500 /1000)
    openGripper()
    sleep(100/1000)

def end():
    gotoHome(True)
    sleep(0.5)
    _baseServo.detach()
    _shoulderServo.detach()
    _elbowServo.detach()
    _gripperServo.detach()
    print('---------------- ARM ENDED ----------------')

def getX():
    return _currentPosition[0]

def getY():
    return _currentPosition[1]

def getZ():
    return _currentPosition[2]

def gotoHome(bInstant = False):
    print('Going home. Instant? ' + str(bInstant))
    if (bInstant): goDirectlyTo(HOME_POS[0], HOME_POS[1], HOME_POS[2])
    else: gotoPoint(HOME_POS[0], HOME_POS[1], HOME_POS[2])

#def convertAngle(angle):
#    return (angle / 180) * 2 - 1

def goDirectlyTo(x, y, z):
    #rotated = ext.rotateVector(x, y, 10)
    #x = rotated[0]
    #y = rotated[1]

    x = ext.clip(x, 0, 200) # avoid points inside the base

    #print('Requested direct: ' + str(x) + ', ' + str(y) + ', ' + str(z))
    tarPos = [x, y, z]
    global _currentPosition # will update this value

    tarX = x + BASE_OFFSET[0]
    tarY = y + BASE_OFFSET[1]
    tarZ = z + BASE_OFFSET[2]

    b = atan2(tarY, tarX) * 57.2958 # base angle

    l = sqrt(tarX * tarX + tarY * tarY) # x and y extension
    h = sqrt(l * l + tarZ * tarZ);

    phi = atan(tarZ / l) * 57.2958
    boo = ext.clip((h / 2.0) / SEGMENT_LENGTH, -1, 1)
    theta = acos(boo) * 57.2958

    a1 = phi + theta # angle for first part of the arm
    a2 = phi - theta # angle for second part of the arm

    #b = 110 + b
    b = 90 + b
    a1 = 180 - a1
    a2 = 90 + a2
    #print('Pushing angles: ' + str(int(b)) + ', ' + str(int(a1)) + ', ' + str(int(a2)))
	# Move to the calculated angles
	# Constraint to safe angles (physically checked servo limits on built arm)
	# Also add offsets to mimic the physical arm
    _baseServo.setAngle(b)
    _shoulderServo.setAngle(a1)
    _elbowServo.setAngle(a2)

	# Update position
    _currentPosition = tarPos

    sleep(_stepInterval)

    # todo add checks
    return True

def gotoPoint(x, y, z):
    print('Going to: ' + str(x) + ', ' + str(y) + ', ' + str(z))
    initX = _currentPosition[0]
    initY = _currentPosition[1]
    initZ = _currentPosition[2]

    # Calculate the distance between the current position and the target point
    #dist = sqrt((initX - x) * (initX - x) + (initY - y) * (initY - y) + (initZ - z) * (initZ - z))
    dist = ext.dist3(initX, x, initY, y, initZ, z)

    # Lerp to the point using step size and step interval
    if (dist > STEP_SIZE): # if the distance is greater than the step size, lerp)
        stepCount = round(dist / STEP_SIZE)
        #print('steps: ' + str(stepCount))
        #print('estimated time: ' + str(stepCount * _stepInterval * 100) + ' milliseconds')
        for i in range(0, stepCount):
            factor = float(i) / float(stepCount)
            goDirectlyTo(initX + (x - initX) * factor, initY + (y - initY) * factor, initZ + (z - initZ) * factor)
            sleep(_stepInterval)
    # make sure we arrive
    goDirectlyTo(x, y, z)

    sleep(ACTIONS_DELAY / 1000)
    # todo add checks for out of range
	# todo add checks for collisions
	# todo add checks for unreachable points
    return True
    
def openGripper():
    print('Opening gripper...')
    global _currentGrip

    _gripperServo.setAngle(GRIP_OPEN_ANGLE)
    _currentGrip = GRIP_OPEN_ANGLE
    #_gripperServo.value = convertAngle(GRIP_OPEN_ANGLE)
    #_currentGrip = GRIP_OPEN_ANGLE
    sleep(ACTIONS_DELAY / 1000)

def closeGripper():
    print('Closing gripper...')
    global _currentGrip

    for i in range(int(GRIP_OPEN_ANGLE), int(GRIP_CLOSE_ANGLE),  int(STEP_SIZE)):
        _gripperServo.setAngle(i)
        sleep(_stepInterval * 2)

    # make sure we arrive
    _gripperServo.setAngle(GRIP_CLOSE_ANGLE)
    #_gripperServo.value = convertAngle(GRIP_CLOSE_ANGLE)
    _currentGrip = GRIP_CLOSE_ANGLE
    sleep(ACTIONS_DELAY / 1000)