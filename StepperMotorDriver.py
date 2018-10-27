import RPi.GPIO as GPIO
import time

class SystemInfoMenu():
    halfstep_seq = [
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 1]
    ]

    def __init__(self, pins):
        self.pins = pins
        GPIO.setmode(GPIO.BOARD)
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)

    def step(self, steps):
        # 512 for one rotation?
        for i in range(steps):
            for halfstep in range(8):
                GPIO.output(self.pins, self.halfstep_seq[halfstep])
                time.sleep(0.001)

    def cleanup(self):
        GPIO.cleanup()
