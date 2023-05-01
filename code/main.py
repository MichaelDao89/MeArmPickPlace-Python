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
from time import sleep

ARM_X_OFFSET =-30    # the sensor position, forward from the base center
ARM_Y_OFFSET = 85   # the sensor position, left from the base center
TARGET_HEIGHT = -30

def main():
    print('Hello Michael')
    phy.begin()
    phy.runTests()

    try:
        if (input('step by step? (y/n): ') == 'y'):
            while True:
                i = input('Scan now? (y/n): ')
                if (i == 'y'):
                    r = phy.scanEnvironment()
                    targetPos = tri.findTarget(r)
                    print('____________________________________________')
                    print('Most likely target position: ' + str(targetPos))

                    if (targetPos is not None):
                        processed = processTargetPos(targetPos)
                        if (processed is not None):
                            i = input('Target found, move arm? (y/n):')
                            if (i == 'y'):
                                phy.armPickUpSequence(processed)

                                i = input('Drop off? (y/n):')
                                if (i == 'y'):
                                    phy.armDropOffSequence([75, -100, 30])
                                else: phy.meArm.openGripper()
                        else: print('Invalid target position, skipping')
        else:
            while True:
                r = phy.scanEnvironment()
                tar = tri.findTarget(r)
                if (tar is not None):
                    processed = processTargetPos(tar)
                    if (processed is not None):
                        phy.armPickUpSequence(processed)
                        phy.armDropOffSequence([75, -100, 30])
                    else: print('Invalid target position, skipping')
                else: 
                    print('No target found, skipping')
                sleep(0.5)
    except KeyboardInterrupt:
        print('Keyboard interrupt detected, ending program')
        phy.end()

def processTargetPos(pos):
    #print('Processing position: ' + str(pos))
    if (pos is None) : return None
    r = []

    # swap x and y
    r.append(pos[1])
    r.append(pos[0] * -1.0)

    # add offset
    r[0] += ARM_X_OFFSET
    r[1] += ARM_Y_OFFSET

    rotated = ext.rotateVector(r[0], r[1], 10)
    r[0] = rotated[0]
    r[1] = rotated[1]

    #print('offset: ' + str(r))
    #r[1] += ext.map(r[1], -10.0, 130.0, 0.0, -15.0)

    # the further away, the lower the arm should go (adjust for physical arm behavior)
    heightOffset = ext.map(ext.dist3(r[0], 0, r[1], 0), 5, 100, 0, -20) 

    r.append(TARGET_HEIGHT + heightOffset)

    print('Processed target pos: ' + str(r))
    if (r[0] < 0): return None # target can't be behind the arm
    return r


if __name__ == "__main__":
    main()

