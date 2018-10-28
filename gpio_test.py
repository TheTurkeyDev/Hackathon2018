import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
pwm1 = GPIO.PWM(19, 50)
pwm2 = GPIO.PWM(18, 50)

pwm1.start(12)
pwm2.start(12)

sleep(5)

pwm1.ChangeDutyCycle(8)
pwm2.ChangeDutyCycle(8)

sleep(5)

pwm1.ChangeDutyCycle(2)
pwm2.ChangeDutyCycle(2)

sleep(5)

pwm1.stop()
pwm2.stop()

GPIO.cleanup()
