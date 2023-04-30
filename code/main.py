# ARM mapping
# 8 - Base (Pin 24)
# 25 - Shoulder (22)
# 24 - Elbow (18)
# 23 - Gripper (16)

# SONAR mapping
# 17 - Neck (Pin 11)
# 27 - Trigger (Pin 13)
# 22 - Echo (Pin 15)

import physical_interface as phy
import triangulation as tri
import my_extension as ext

ARM_X_OFFSET = -20    # the sensor position, forward from the base center
ARM_Y_OFFSET = 110   # the sensor position, left from the base center
TARGET_HEIGHT = 0

def main():
    print('Hello Michael')
    phy.begin()
    phy.runTests()

    try:
        while True:
            i = input('Scan now? (y/n): ')
            if (i == 'y'):
                r = phy.scanEnvironment()
                targetPos = tri.findTarget(r)
                print('____________________________________________')
                print('Most likely target position: ' + str(targetPos))

                if (targetPos is not None):
                    processed = processTargetPos(targetPos)
                    print('Processed target position: ' + str(processed))
                    i = input('Target found, move arm? (y/n):')
                    if (i == 'y'):
                        phy.armPickUpSequence(processed)
                        phy.armDropOffSequence([50, -50, 0])
    except KeyboardInterrupt:
        print('Keyboard interrupt detected, ending program')
        phy.end()

def processTargetPos(pos):
    #print('Processing position: ' + str(pos))

    r = []

    # swap x and y
    r.append(pos[1])
    r.append(pos[0] * -1.0)

    # add offset
    r[0] += ARM_X_OFFSET
    r[1] += ARM_Y_OFFSET

    #print('offset: ' + str(r))
    #r[1] += ext.map(r[1], -40.0, 250.0, -10.0, 50)

    print('final: ' + str(r))
    r.append(TARGET_HEIGHT)

    return r


if __name__ == "__main__":
    main()

