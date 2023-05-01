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
from me_arm_driver import ACTIONS_DELAY
import sonar_driver as sonar

pins = (8, 25, 24, 23)

def begin():
    print('---------------- PHYSICAL PERIPHERAL BEGIN ----------------')
    pwm = pigpio.pi()

    meArm.begin(pwm, 8, 25, 24, 23)
    sonar.begin(pwm, 17, 27, 22)
    sleep(0.5)

def end():
    meArm.end()
    sonar.end()
    print('---------------- PHYSICAL PERIPHERAL ENG ----------------')

def scanEnvironment():
    print('---------------- SCANNING ENVIRONMENT ----------------')
    return sonar.scan()
    print('---------------- SCAN ENVIRONMENT ENDED ----------------')

def armPickUpSequence(position):
    print('---------------- GOING TO PICKUP ----------------')
    sleep(ACTIONS_DELAY / 1000) # make sure all existing movements are completed

    # Go to prep position
    meArm.openGripper()
    meArm.gotoPoint(20, -10, 50)
    #sleep(0.2)
    meArm.gotoPoint(position[0] - 20, position[1] - 20, 30)
    sleep(ACTIONS_DELAY/ 1000)

    # Go to target position
    meArm.gotoPoint(position[0] + 5, position[1], position[2])
    sleep(ACTIONS_DELAY/ 1000)

    # Pick up
    meArm.closeGripper()
    sleep(ACTIONS_DELAY * 5 / 1000)

    meArm.gotoHome()
    print('---------------- PICKED UP ----------------')
    

def armDropOffSequence(position):
    print('---------------- GOING TO DROP OFF ----------------')
    sleep(ACTIONS_DELAY/ 1000) # make sure all existing movements are completed

    # Go to drop off position
    meArm.gotoPoint(position[0], position[1], position[2])
    sleep(ACTIONS_DELAY/ 1000)

    # Drop off
    meArm.openGripper()
    sleep(0.2)

    # Lift arm up
    meArm.gotoPoint(position[0] - 10, position[1], position[2] + 100)
    sleep(ACTIONS_DELAY/ 1000)

    # Return to home
    meArm.gotoHome()
    print('---------------- DROPPED OFF ----------------')

def runTests():
    print('---------------- PERIPHERAL TESTS BEGIN ----------------')
    try:
        i = input("Begin test? (y/n):")
        while (i == "y"):
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
            i = input("retest? (y/n):")
        print('---------------- EXIT TESTS ----------------')
        return
    except KeyboardInterrupt:
        print('---------------- TESTS INTERRUPTED ----------------')
        return

def testArm():
    print('---------------- ARM TEST BEGIN ----------------')
    startX = input('Starting x: ')
    startY = input('Starting y: ')
    startZ = input('Starting z: ')
    extend = input('Extend (10-150): ')
    
    
    startX = float(startX)
    startY = float(startY)
    startZ = float(startZ)
    extend = float(extend)

    testY = input('test Y? (y/n): ')
    if (testY == 'y'):
        repeat = 'y'
        while (repeat == 'y'):
            print('Arm lerping Y')
            meArm.gotoPoint(startX, startY, startZ)
            meArm.gotoPoint(startX, startY + extend, startZ)
            cont = 'n'
            while cont != 'y': 
                cont = input('Continue? (y/n): ')
            meArm.gotoPoint(startX, startY - extend, startZ)
            sleep(0.5)
            repeat = input('Repeat? (y/n): ')

    testX = input('test X? (y/n): ')
    if (testX == 'y'):
        repeat = 'y'
        while (repeat == 'y'):
            meArm.gotoPoint(startX, startY, startZ)
            print('Arm lerping X')
            meArm.gotoPoint(startX + extend, startY, startZ)
            cont = 'n'
            while cont != 'y': 
                cont = input('Continue? (y/n): ')
            meArm.gotoPoint(5, startY, startZ)
            sleep(0.5)
            repeat = input('Repeat? (y/n): ')

    testZ = input('test z? (y/n): ')
    if (testZ == 'y'):
        repeat = 'y'
        while (repeat == 'y'):
            meArm.gotoPoint(startX, startY, startZ)
            print('Arm lerping Z')
            meArm.gotoPoint(startX, startY, startZ + extend)
            cont = 'n'
            while cont != 'y': 
                cont = input('Continue? (y/n): ')
            meArm.gotoPoint(startX, startY, startZ + extend)
            sleep(0.5)
            repeat = input('Repeat? (y/n): ')

    testPos = input('Test positions? (y/n): ')
    while (testPos == 'y'):
        print('Testing positions')
        x = float(input('X: '))
        y = float(input('Y: '))
        z = float(input('Z: '))
        go = input('Go to position? (y/n): ')
        if (go == 'y'):
            meArm.gotoPoint(x, y, z)
            testPos = input('Test another position? (y/n): ')

    testCombined = input('Test combined? (y/n): ')
    if (testCombined == 'y'):
        meArm.gotoHome()
        print('Arm picking up')
        meArm.gotoPoint(70, 70, 0)
        sleep(0.2)
        meArm.openGripper()
        meArm.closeGripper()
        sleep(0.2)
        meArm.gotoPoint(50, -100, 50)
        sleep(0.5)

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

    
