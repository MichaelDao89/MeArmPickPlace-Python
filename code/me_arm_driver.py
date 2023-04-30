# ARM mapping
# (BCM num:) 8 - Base (Board num: 24)
# 25 - Shoulder (22)
# 24 - Elbow (18)
# 23 - Gripper (16)

from math import acos, atan, atan2, sqrt
import my_extension as ext
#from gpiozero import Servo
#import RPi.GPIO as GPIO
import pigpio
from time import sleep

############## CONSTANTS ##############
# You can work in any units, as long as they all match; these
# will dictate the units of the 3D space you're in.  I used millimetres.
SEGMENT_LENGTH = 80; # e.g., shoulder to elbow length
# X: avoid points inside the base, this moves X = 0 to the edge of the meArm base
# Y: use this to adjust sideway offsets
# Z: account for base to shoulder joint offset, this moves Z = 0 to the floor level of the meArm base
BASE_OFFSET = (0, 0, -30); 
STEP_SIZE = 1.0; # movement delta when lerping, in mm, lower value = higher step fidelity
SPEED = 50.0; # movement speed, in cm/seconds
ACTIONS_DELAY = 100.0; # delay between actions, in milliseconds

# Default angles
HOME_POS = [50, 0, 50]
GRIP_OPEN_ANGLE = 155;
GRIP_CLOSE_ANGLE = 120;

############### RUNTIME ###############
_baseServo, _shoulderServo, _elbowServo, _gripperServo = None, None, None, None
_currentPosition, _currentGrip = None, None
_stepInterval = None

class Servo():
    def __init__(self, pin, pwm, minPWM = 1000, maxPWM = 2000, minAngle = 0, maxAngle = 180):
        self.pin = pin
        self.pwm = pwm
        self.minPWM = minPWM
        self.maxPWM = maxPWM
        self.minAngle = minAngle
        self.maxAngle = maxAngle

    def setAngle(self, angle):
        #print(str(self.minPWM))
        angle = ext.clip(angle, self.minAngle, self.maxAngle)
        self.pwm.set_servo_pulsewidth(
            self.pin, 
            ext.map(angle, self.minAngle, self.maxAngle, self.minPWM, self.maxPWM)
            )

    def detach(self):
        self.pwm.set_PWM_dutycycle(self.pin, 0)
        self.pwm.set_PWM_frequency(self.pin, 0)

def begin(pwm, basePin, shoulderPin, elbowPin, gripperPin):
    # will change these values
    global _baseServo, _shoulderServo, _elbowServo, _gripperServo
    global _stepInterval

    # Attach the servos
    if (_baseServo is None):
        pwm.set_mode(basePin, pigpio.OUTPUT)
        pwm.set_PWM_frequency(basePin, 50)
        _baseServo = Servo(basePin, pwm, 1000, 2000, 0, 180)
        #_baseServo = Servo(basePin, 0, 0.750/1000, 2.250/1000)
    if (_shoulderServo is None):
        pwm.set_mode(shoulderPin, pigpio.OUTPUT)
        pwm.set_PWM_frequency(shoulderPin, 50)
        _shoulderServo = Servo(shoulderPin, pwm, 900, 2100, 20, 160)
        #_shoulderServo = Servo(shoulderPin, 0, 0.9/1000, 2.100/1000)
    if (_elbowServo is None):
        pwm.set_mode(elbowPin, pigpio.OUTPUT)
        pwm.set_PWM_frequency(elbowPin, 50)
        _elbowServo = Servo(elbowPin, pwm, 750, 2250, 0, 180)
        #_elbowServo = Servo(elbowPin, 0, 0.750/1000, 2.250/1000)
    if (_gripperServo is None):
        pwm.set_mode(gripperPin, pigpio.OUTPUT)
        pwm.set_PWM_frequency(gripperPin, 50)
        _gripperServo = Servo(gripperPin, pwm, 460, 2400, 30, 150)
        #_gripperServo = Servo(gripperPin, 0, 0.460/1000, 2.400/1000)
    print('---------------- ARM BEGIN ----------------')
    print('Servos attached')

    # Calculate dynamic constants
    _stepInterval = (STEP_SIZE / (SPEED * 0.01)) / 1000
    #_stepInterval = 50 / 1000
    print('Step interval: ' + str(_stepInterval * 1000) + ' milliseconds')

    gotoHome(True)
    sleep(200/1000)

def end():
    gotoHome(True)
    sleep(0.5)
    _baseServo.detach()
    _shoulderServo.detach()
    _elbowServo.detach()
    _gripperServo.detach()
    print('---------------- ARM ENDED ----------------')

def gotoHome(bInstant = False):
    print('Going home. Instant? ' + str(bInstant))
    if (bInstant): goDirectlyTo(HOME_POS[0], HOME_POS[1], HOME_POS[2])
    else: gotoPoint(HOME_POS[0], HOME_POS[1], HOME_POS[2])

#def convertAngle(angle):
#    return (angle / 180) * 2 - 1

def goDirectlyTo(x, y, z):
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
    theta = acos((h / 2) / SEGMENT_LENGTH) * 57.2958

    a1 = phi + theta # angle for first part of the arm
    a2 = phi - theta # angle for second part of the arm

    b = 110 + b
    a1 = 180 - a1
    a2 = 90 + a2
    print('Pushing angles: ' + str(int(b)) + ', ' + str(int(a1)) + ', ' + str(int(a2)))
	# Move to the calculated angles
	# Constraint to safe angles (physically checked servo limits on built arm)
	# Also add offsets to mimic the physical arm
    _baseServo.setAngle(b)
    _shoulderServo.setAngle(a1)
    _elbowServo.setAngle(a2)

    #_baseServo.value = convertAngle(b)
    #_shoulderServo.value = convertAngle(a1)
    #_elbowServo.value = convertAngle(a2)

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
    dist = sqrt((initX - x) * (initX - x) + (initY - y) * (initY - y) + (initZ - z) * (initZ - z))

    # Lerp to the point using step size and step interval
    if (dist > STEP_SIZE): # if the distance is greater than the step size, lerp)
        stepCount = round(dist / STEP_SIZE)
        for i in range(0, stepCount):
            factor = float(i) / float(stepCount)
            goDirectlyTo(initX + (x - initX) * factor, initY + (y - initY) * factor, initZ + (z - initZ) * factor)
            sleep(_stepInterval)

        #for i in range(0, int(dist / STEP_SIZE)):
        #    newX = initX + (x - initX) * (i * STEP_SIZE / dist)
        #    newY = initY + (y - initY) * (i * STEP_SIZE / dist)
        #    newZ = initZ + (z - initZ) * (i * STEP_SIZE / dist)
        #    goDirectlyTo(newX, newY, newZ)
        #    sleep(_stepInterval)

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

    # lerp gripper using step size and step interval
    for i in range(0, int((GRIP_CLOSE_ANGLE - _currentGrip) / STEP_SIZE)):
        _gripperServo.setAngle(i)
        #_gripperServo.value = convertAngle(_currentGrip + i * STEP_SIZE)
        sleep(_stepInterval)

    # make sure we arrive
    _gripperServo.setAngle(GRIP_CLOSE_ANGLE)
    #_gripperServo.value = convertAngle(GRIP_CLOSE_ANGLE)
    _currentGrip = GRIP_CLOSE_ANGLE
    sleep(ACTIONS_DELAY / 1000)