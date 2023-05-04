import RPi.GPIO as GPIO
import pigpio
from time import sleep, time
import my_extension as ext

STEP_SIZE = 5; # movement delta when lerping, in degree, lower value = higher step fidelity
_stepInterval = 0.05 # in seconds, calculated based on speed
_sonarTimeout = 0.05 # in seconds, calculated based on maxRange
_neckPWM = None

# speed in degrees per seconds
# range in millimeters
# rotation in degrees
def begin(pwm, neckPin, triggerPin, echoPin, speed = 270, minRotation = 30, maxRotation = 150, minRange = 50, maxRange = 500):
	global _neckPWM, _minRotation, _maxRotation, _minRange, _maxRange	# values
	global _neckPin, _triggerPin, _echoPin	# pins
	global _stepInterval, _sonarTimeout	   # calculated values

	_minRotation = minRotation
	_maxRotation = maxRotation
	_minRange = minRange
	_maxRange = maxRange
	_stepInterval = (1 / (speed / STEP_SIZE))
	_sonarTimeout = (((_maxRange + 10) / 1000) / (343 / 2.0))
	#print('timeout: ' + str(_sonarTimeout))

	# save pins
	_neckPin = neckPin
	_triggerPin = triggerPin
	_echoPin = echoPin

	# set up pin
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(_triggerPin, GPIO.OUT)
	GPIO.output(_triggerPin, GPIO.LOW)
	GPIO.setup(_echoPin, GPIO.IN)

	# set up neck
	_neckPWM = pwm
	_neckPWM.set_mode(_neckPin, pigpio.OUTPUT)
	_neckPWM.set_PWM_frequency(_neckPin, 50)

def scan():
	return rotate360(measureDistance)

def end():
    _neckPWM.set_servo_pulsewidth(_neckPin, 0)
    GPIO.cleanup()

################################ INTERNAL methods ################################
# return results in a list of tuples
#  containing (angle, the returns from functions)
def rotate360(delegate = None):
	results = []

	# from center to max
	for i in range(90, _minRotation, -STEP_SIZE):
		setNeckAngle(i)
		sleep(_stepInterval)

	for i in range(_minRotation, _maxRotation, STEP_SIZE):
		setNeckAngle(i)
		if (delegate is not None):
			results.append((i, delegate()))
		sleep(_stepInterval)

	for i in range(_maxRotation, _minRotation, -STEP_SIZE):
		setNeckAngle(i)
		if (delegate is not None):
			results.append((i, delegate()))
		sleep(_stepInterval)

	# return to center
	for i in range(_minRotation, 90, STEP_SIZE):
		setNeckAngle(i)
		sleep(_stepInterval)

	# return to center
	_neckPWM.set_servo_pulsewidth(_neckPin, ext.map(90, 0, 180, 600, 2400))
	return results

def setNeckAngle(i):
	_neckPWM.set_servo_pulsewidth(_neckPin, ext.map(i, 0, 180, 600, 2400))

# returns distance in millimeters
def measureDistance():
	GPIO.output(_triggerPin, True)
	sleep(0.00001)
	GPIO.output(_triggerPin, False)

	startTime = time()
	stopTime = time()

	# wait for echo to go high
	while (GPIO.input(_echoPin) == 0):
		startTime = time()
		
	# wait for the echo to go low again
	while (GPIO.input(_echoPin) == 1):
		#print('stopping')
		stopTime = time()
		if (time() - startTime) > _sonarTimeout:
			return 0

	# when the echo has gone high and back to low, stop the timer
	# calculate distance based on time elapsed
	timeElapsed = stopTime - startTime
	#print('-----------------------------')
	dis = round(timeElapsed * 343000.0 / 2.0, 2)

	if (dis < _minRange or dis > _maxRange):
		return 0
	else:
		return round(timeElapsed * 343000.0 / 2.0, 2)

################################ TEST methods ################################
def testNeckRotation():
	print('--Testing neck rotation--')
    # rotate neck
	rotate360()
	print('--Finished testing neck rotation--')

def testDistanceMeasuring():
	print('--Testing distance measuring--')
	print('Distance: ' + str(measureDistance()))
	print('--Finished distance measuring--')

def testIntegration():
	print('--Testing distance measuring--')

	# start looping
	delegates = [measureDistance]
	for i in range(0, 2):
		r = rotate360(delegates)
		print(r)
		#if (_callback is not None):
		#	_callback(r)

	print('--Finished distance measuring--')



