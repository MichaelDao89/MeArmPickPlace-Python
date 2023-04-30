# ARM mapping
# (BCM num:) 8 - Base (Board num: 24)
# 25 - Shoulder (22)
# 24 - Elbow (18)
# 23 - Gripper (16)

# SONAR mapping
# 17 - Neck (Pin 11)
# 27 - Trigger (Pin 13)
# 22 - Echo (Pin 15)

#from gpiozero import Servo
import pigpio
from time import sleep
import me_arm_driver as meArm
import sonar_driver as sonar

pins = (8, 25, 24, 23)

def begin():
    print('---------------- PHYSICAL PERIPHERAL BEGIN ----------------')
    pwm = pigpio.pi()

    meArm.begin(pwm, 8, 25, 24, 23)
    sonar.begin(pwm, 17, 27, 22, resultCallback=processSonarResult)
    sleep(0.5)

    while (True):
        i = input("Test arm? (y/n): ")
        if i == 'y':
            testArm()
        else:
            i = input("Test sonar? (y/n): ")

            if i == 'y':
                i = input("Test type? (i - integration, r - neck rotation, d - distance): ")
                if (i == 'i'):
                    sonar.testIntegration()
                elif (i == 'r'):    
                    sonar.testNeckRotation()
                elif (i == 'd'):
                    sonar.testDistanceMeasuring()
                #print('Need refactoring...')
                #tri.test()
            #testArmServos()
    #testArm()

def printResult(r):
    print(r)

def processSonarResult(r):
    print(r)

def end():

    print('---------------- PHYSICAL PERIPHERAL ENG ----------------')

def testArm():
    print('---------------- ARM TEST BEGIN ----------------')
    print('Arm lerping Y')
    meArm.gotoPoint(25, 120, 30)
    sleep(2)
    meArm.gotoPoint(25, -120, 30)
    sleep(1)

    meArm.gotoHome()
    print('Arm lerping X')
    meArm.gotoPoint(130, 0, 30)
    sleep(2)
    meArm.gotoPoint(5, 0, 30)
    sleep(1)

    meArm.gotoHome()
    print('Arm lerping Z')
    meArm.gotoPoint(25, 0, 0)
    sleep(2)
    meArm.gotoPoint(25, 0, 150)
    sleep(1)

    meArm.gotoHome()
    print('Arm picking up')
    meArm.gotoPoint(70, 70, 0)
    sleep(0.5)
    meArm.openGripper()
    meArm.closeGripper()
    sleep(0.5)
    meArm.gotoPoint(50, -100, 50)
    sleep(1)

    meArm.gotoHome()
    meArm.end()
    print('---------------- ARM TEST ENDED ----------------')

#def testArmServos():
#    accept = 'y'
#    while (accept == 'y'):
#        user_input = input("Which servo to test? (b/s/e/g/combo): ")
#        if user_input == 'b':
#            testServo(8, 750, 2500, 20, 160)

#        elif user_input == 's':
#            testServo(25, 900, 2100, 20, 160)

#        elif user_input == 'e':
#            testServo(24, 900, 2100, 20, 160)

#        elif user_input == 'g':
#            testServo(23, 460, 2400, 130, 160, 145)

#        elif user_input == 'combo':
#            print('This only tests the power capability using the standard pwm range (1000-2000microsecs) and 20-160 angles for safety.')
#            user_input = input('Servo count? (1-4)')
#            if user_input == '1' or user_input == '2' or user_input == '3' or user_input == '4':
#                testServoMulti(int(user_input))
#            else: print('Invalid input')
#        else:
#            print('Invalid input')
#        accept = input("retest arm servos? (y/n): ")

#def testServoMulti(count):
#    print('---------------- SERVO MULTI TEST BEGIN ----------------')
#    print('Target pins: ' + str(pins))
#    mindeg = 20
#    maxdeg = 160
#    startdeg = 90
#    interval = 0.03

#    servos = []
#    servos.append(Servo(pins[0], 0, 1000/1000000, 2000/1000000))
#    servos.append(Servo(pins[1], 0, 1000/1000000, 2000/1000000))
#    servos.append(Servo(pins[2], 0, 1000/1000000, 2000/1000000))
#    servos.append(Servo(pins[3], 0, 1000/1000000, 2000/1000000))
#    sleep(1)

#    #lerp from 0 to mindeg
#    print('Going to mindeg: ' + str(mindeg))
#    for i in range(startdeg, mindeg, -1):
#        for j in range(count):
#            print(j)
#            servos[j].value = (i / 180) * 2 - 1
#        sleep(interval)

#    print('Full range lerp: ')
#    #lerp full range
#    for i in range(mindeg, maxdeg):
#        for j in range(count):
#            servos[j].value = (i / 180) * 2 - 1
#        print('Deg: ' + str(i) + '. Val: ' + str(servos[0].value))
#        sleep(interval)

#    # return home
#    print('Peaceful return...')
#    for i in range(maxdeg, startdeg, -1):
#        for j in range(count - 1):
#            servos[j].value = (i / 180) * 2 - 1
#        sleep(interval)
    
#    print('Detaching...')
#    sleep(0.2)
#    for i in range(count):
#        servos[i].detach()
#    print('Detached all servos.')
#    print('|_______________ SERVO TEST ENDED _______________|')

#def testServo(pin, minPwm, maxPwm, mindeg = 20.0, maxdeg = 160.0, startdeg = 90):
#    print('---------------- SERVO TEST BEGIN ----------------')
#    print('Target pin: ' + str(pin))
#    s = Servo(pin, 0, minPwm/1000000, maxPwm/1000000)
#    sleep(1)

#    #lerp from 0 to mindeg
#    print('Going to mindeg: ' + str(mindeg))
#    for i in range(startdeg, mindeg, -1):
#        s.value = (i / 180) * 2 - 1
#        sleep(0.015)

#    print('Full range lerp: ')
#    #lerp full range
#    for i in range(mindeg, maxdeg):
#        s.value = (i / 180) * 2 - 1
#        print('Deg: ' + str(i) + '. Val: ' + str(s.value))
#        sleep(0.015)

#    # return home
#    print('Peaceful return...')
#    for i in range(maxdeg, startdeg, -1):
#        s.value = (i / 180) * 2 - 1
#        sleep(0.015)
    
#    print('Detaching...')
#    sleep(0.1)
#    s.detach()
#    print('|_______________ SERVO TEST ENDED _______________|')

    
