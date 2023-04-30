import RPi.GPIO as GPIO
import pigpio
from time import sleep, time
import my_extension as ext
from typing import Callable

STEP_SIZE = 2; # movement delta when lerping, in degree, lower value = higher step fidelity
_stepInterval = 0.05 # in seconds, calculated based on speed
_sonarTimeout = 0.05 # in seconds, calculated based on maxRange
_neckPWM = None
_isPaused = False
_callback = None

# speed in degrees per seconds
# range in millimeters
# rotation in degrees
def begin(pwm, neckPin, triggerPin, echoPin, speed = 270, minRotation = 0, maxRotation = 180, minRange = 5, maxRange = 300, resultCallback = None):
	global _neckPWM, _minRotation, _maxRotation, _minRange, _maxRange	# values
	global _neckPin, _triggerPin, _echoPin	# pins
	global _stepInterval, _sonarTimeout, _callback	   # calculated values

	_minRotation = minRotation
	_maxRotation = maxRotation
	_minRange = minRange
	_maxRange = maxRange
	_stepInterval = (1 / (speed / STEP_SIZE))
	_sonarTimeout = (((_maxRange + 10) / 1000) / (343 / 2.0))
	print('timeout: ' + str(_sonarTimeout))

	# setup pins
	GPIO.setmode(GPIO.BCM)
	_neckPin = neckPin
	_triggerPin = triggerPin
	_echoPin = echoPin

	_neckPWM = pwm
	_neckPWM.set_mode(_neckPin, pigpio.OUTPUT)
	_neckPWM.set_PWM_frequency(_neckPin, 50)

	GPIO.setup(_triggerPin, GPIO.OUT)
	GPIO.output(_triggerPin, GPIO.LOW)
	GPIO.setup(_echoPin, GPIO.IN)

	if (resultCallback is not None):
		_callback = resultCallback
	## start looping
	#delegates = [measureDistance]
	#while (not _isPaused):
	#	rotate360(delegates)

def pause():
    _isPaused = True

def unpause():
	_isPaused = False

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
	return round(timeElapsed * 343000.0 / 2.0, 2)

def parseResults(results):
	print('to be implemented')

# return results in a list of tuples
#  containing (angle, the returns from functions)
def rotate360(delegates = None):
	results = []

	for i in range(_minRotation, _maxRotation, STEP_SIZE):
		_neckPWM.set_servo_pulsewidth(_neckPin, ext.map(i, _minRotation, _maxRotation, 1000, 2000))

		# execute functions
		if (delegates is not None):
			functionResults = []
			for function in delegates:
				functionResults.append(function())
			results.append([i, functionResults])

		sleep(_stepInterval)

	for i in range(_maxRotation, _minRotation, -STEP_SIZE):
		_neckPWM.set_servo_pulsewidth(_neckPin, ext.map(i, _minRotation, _maxRotation, 1000, 2000))

		# execute functions
		if (delegates is not None):
			functionResults = []
			for function in delegates:
				functionResults.append(function())
			results.append([i, functionResults])

		sleep(_stepInterval)

	return results

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
		if (_callback is not None):
			_callback(r)

	print('--Finished distance measuring--')



