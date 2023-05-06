import my_extension as ext
import pigpio

class Servo():
    def __init__(self, pin, pwm, minPWM = 1000, maxPWM = 2000, minAngle = 0, maxAngle = 180):
        self.pin = pin
        self.pwm = pwm
        self.minPWM = minPWM
        self.maxPWM = maxPWM
        self.minAngle = minAngle
        self.maxAngle = maxAngle

    def setAngle(self, angle):
        #print(str(self.minPWM))
        angle = ext.clip(angle, self.minAngle, self.maxAngle)
        self.pwm.set_servo_pulsewidth(
            self.pin, 
            ext.map(angle, self.minAngle, self.maxAngle, self.minPWM, self.maxPWM)
            )

    def detach(self):
        self.pwm.set_PWM_dutycycle(self.pin, 0)
        self.pwm.set_PWM_frequency(self.pin, 0)