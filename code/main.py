# ARM mapping
# 8 - Base (Pin 24)
# 25 - Shoulder (22)
# 24 - Elbow (18)
# 23 - Gripper (16)

# SONAR mapping
# 17 - Neck (Pin 11)
# 27 - Trigger (Pin 13)
# 22 - Echo (Pin 15)

import webserver.webmanager as web
import physical_interface as phy
import triangulation as tri
import my_extension as ext
from time import sleep
import os

ARM_X_OFFSET =-30    # the sensor position, forward from the base center
ARM_Y_OFFSET = 85   # the sensor position, left from the base center
TARGET_HEIGHT = -30

PATH_PREFIX = "/home/piMD/MeArm/code/webserver/"
OUTPUT_PATH = PATH_PREFIX + "static/images/scan_output/"

def main():
    # clean up scan_output on startup
    for filename in os.listdir(OUTPUT_PATH):
        file_path = os.path.join(OUTPUT_PATH, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"{filename} deleted successfully")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

    web.startServer()
    print('Hello Michael')
    phy.begin()

    try:
        while True:
            print('-------------------- SEQUENCE BEGINS --------------------')
            r = phy.scanEnvironment()

            tar = tri.findTarget(r)
            print('-------------------- SCAN COMPLETED --------------------')
            web.updateOutput(tri.getLatestURL())

            # delay pickup to allow the user to see the scan result
            sleep(0.5)
            if (tar is not None):
                print('-------------------- ARM ACTIVATED --------------------')
                processed = processTargetPos(tar)
                if (processed is not None):
                    phy.armPickUpSequence(processed)
                    phy.armDropOffSequence([75, -100, 30])
                else: print('Invalid target position, skipping')
            else: 
                print('No target found, skipping')

            print('-------------------- RESTARTING SEQUENCE --------------------')
            # delay between scans
            sleep(1)
    except KeyboardInterrupt:
        print('-------------------- Keyboard interrupt detected, ending program --------------------')
        phy.end()

    #phy.runTests()
    #try:
    #    runArm()
    #except KeyboardInterrupt:
    #    print('Keyboard interrupt detected, ending program')
    #    phy.end()

def runArm():
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
            web.updateOutput(tri.getLatestURL())

            # delay pickup to allow the user to see the scan result
            sleep(0.5)
            if (tar is not None):
                processed = processTargetPos(tar)
                if (processed is not None):
                    phy.armPickUpSequence(processed)
                    phy.armDropOffSequence([75, -100, 30])
                else: print('Invalid target position, skipping')
            else: 
                print('No target found, skipping')

            # delay between scans
            sleep(1)

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

