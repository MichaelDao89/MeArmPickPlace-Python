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

def main():
    print('Hello Michael')
    phy.begin()

if __name__ == "__main__":
    main()


