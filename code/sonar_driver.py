import RPi.GPIO as GPIO
import time

_speed = 1
_stepInterval = 15
_minRotation = 20
_maxRotation = 160
_minRange = 5
_maxRange = 20
_pwm = None
_neckPin = 0
_triggerPin = 0
_echoPin = 0

# speed in degrees per millisecond
def begin(neckPin, triggerPin, echoPin, speed, minRotation, maxRotation, minRange, maxRange):
	_speed = speed
	_minRotation = minRotation
	_maxRotation = maxRotation
	_minRange = minRange
	_maxRange = maxRange

	# setup pins
	GPIO.setmode(GPIO.BCM)
	_neckPin = neckPin
	_triggerPin = triggerPin
	_echoPin = echoPin

	GPIO.setup(_neckPin, GPIO.OUT)
	GPIO.setup(_triggerPin, GPIO.OUT)
	GPIO.setup(_echoPin, GPIO.IN)

	GPIO.output(_triggerPin, GPIO.LOW)



