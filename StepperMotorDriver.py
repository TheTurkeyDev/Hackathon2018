import RPi.GPIO as GPIO
import time

class StepperMotorDriver():
    halfstep_for = [
        [1, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 1, 0, 1],
        [1, 0, 0, 1]
    ]

    halfstep_rev = list(reversed(halfstep_for))

    steps_per_rotation = 512;
    steps_per_deg = steps_per_rotation/360
    deg_per_step = 360/steps_per_rotation

    angle = 0

    def __init__(self, pins):
        self.pins = pins
        GPIO.setmode(GPIO.BCM)
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)

    def step(self, steps):
        for i in range(abs(steps)):
            for halfstep in range(4):
                if steps > 0:
                    GPIO.output(self.pins, self.halfstep_for[halfstep])
                else:
                    GPIO.output(self.pins, self.halfstep_rev[halfstep])
                time.sleep(0.005)
            if steps > 0:
                self.angle += self.deg_per_step
            else:
                self.angle -= self.deg_per_step


    def move_to(self, angle):
         steps = int((angle - self.angle) / self.deg_per_step)
         self.step(steps)


    def cleanup(self):
        GPIO.cleanup()
