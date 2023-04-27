# import libraries
from gpiozero import Servo
from time import sleep

# set pin GPIO 17 as control pin for the servo
servoPin = 8

# define functions for positioning the servo 
def servoMid():
    servo.mid()
    print("Set to middle position")
    sleep(2)
    
def servoMin():
    servo.min()
    print("Set to minimum position")
    sleep(2)
    
def servoMax():
    servo.max()
    print("Set to maximum position")
    sleep(2)

# while loop for servo range correction
while True:
    pinInput = input("Enter servo pin: ")
    servoPin = int(pinInput)

    # initial values for min_pulse_width and max_pulse_width
    minPW = 0
    maxPW = 0
    
    # enter a value in a range from 0 to 1 and convert it to a float
    servoCorrection = float(input("Enter correction value: "))
    
    # convert min and max pulse widths into milliseconds
    minPW = (1.0 - servoCorrection)/1000
    maxPW = (2.0 + servoCorrection)/1000
    
    # apply new settings for the servo
    servo = Servo(servoPin, min_pulse_width = minPW, max_pulse_width = maxPW)
    
	# display applied settings
    print("Using GPIO17")
    print("Min pulse width is set to " + str(minPW * 1000) + " ms")
    print("Max pulse width is set to " + str(maxPW * 1000) + " ms")
   
    # move the servo from mid position to min, then back to mid, to max and again to mid
    servoMid()
    servoMin()
    servoMid()
    servoMax()
    servoMid()

	# ask if the correction value is right   
    correctionStatus = int(input('Is this correction value right?' + '\n' + 'If Yes press 1, if No press 0: '))
        
    # if the value is right show the message and break the loop
    if correctionStatus == 1:
        print("Correction's been done")
        break
    
	# otherwise reset the servo and go to the beginning of the loop
    else:
        print("Let's try again")
        servo.close()
        continue

# reset the servo after quitting the loop
servo.close()