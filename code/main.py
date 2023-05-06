import my_extension as ext
from time import sleep, strftime
import os
import webserver.webmanager as web
import physical_interface as phy
import processors.triangulation as tri

ARM_X_OFFSET =-30    # the sensor position, forward from the base center
ARM_Y_OFFSET = 85   # the sensor position, left from the base center
TARGET_HEIGHT = -30

PATH_PREFIX = "/home/piMD/MeArm/code/webserver/"
OUTPUT_PATH = PATH_PREFIX + "static/images/scan_output/"

flag = True

def startSys():
    global flag

    if (flag is False): return
    printWeb('System STARTED at ' + strftime("%H:%M:%S") + '<br>')
    flag = False


def stopSys():
    global flag

    if (flag is True): return
    printWeb('System STOPPED at ' + strftime("%H:%M:%S") + '<br>')
    flag = True

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

    # Run arm
    printWeb('___________________________')
    printWeb('Collecting data...')
    r = phy.scanEnvironment()

    printWeb('Analysing data...')
    tar = tri.findTarget(r)
    web.updateOutput(tri.getLatestURL())

    # delay pickup to allow the user to see the scan result
    sleep(1)
    if (tar is not None):
        processed = processTargetPos(tar)
        if (processed is not None):
            simplified = [round(processed[0]), round(processed[1]), round(processed[2])]
            printWeb('Target found at: ' + str(simplified) + '. Sending command to arm.')
            phy.armPickUpSequence(processed)
            phy.armDropOffSequence([75, -100, 30])
        else: 
            printWeb('Invalid target position. Moving on.')

    else: 
        printWeb('No target found. Moving on.')

    # delay between scans
    printWeb('_______ Restarting ________' + '<br>')
    return

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

    # the further away, the lower the arm should go (adjust for physical arm behavior)
    heightOffset = ext.map(ext.dist3(r[0], 0, r[1], 0), 5, 100, 0, -30) 

    r.append(TARGET_HEIGHT + heightOffset)

    print('Processed target pos: ' + str(r))
    if (r[0] < 0): return None # target can't be behind the arm
    return r

def printWeb(msg):
    print(msg)
    web.add_msg(msg)

if __name__ == "__main__":
    web.startServer(startSys, stopSys)
    phy.begin()
    printWeb('Main started. Awaiting user input...')

    # main loop
    try:
        while True:
            while flag == False:
                main()
                sleep(0.5)
            sleep(0.1)
    except KeyboardInterrupt:
        phy.end()

