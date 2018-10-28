import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
from time import sleep

lcd_rs = 27  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en = 22
lcd_d4 = 25
lcd_d5 = 24
lcd_d6 = 23
lcd_d7 = 18
lcd_backlight = 4
lcd_columns = 16
lcd_rows = 2

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers
GPIO.setup(lcd_en, GPIO.OUT)  # E
GPIO.setup(lcd_rs, GPIO.OUT)  # RS
GPIO.setup(lcd_d4, GPIO.OUT)  # DB4
GPIO.setup(lcd_d5, GPIO.OUT)  # DB5
GPIO.setup(lcd_d6, GPIO.OUT)  # DB6
GPIO.setup(lcd_d7, GPIO.OUT)  # DB7

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

print("Stage 1")
# Print a two line message
lcd.message('Hello\nworld!')

# Wait 5 seconds
sleep(5.0)
print("Stage 2")

# Demo showing the cursor.
lcd.clear()
lcd.show_cursor(True)
lcd.message('Show cursor')

sleep(5.0)
print("Stage 3")

# Demo showing the blinking cursor.
lcd.clear()
lcd.blink(True)
lcd.message('Blink cursor')

sleep(5.0)
print("Stage 4")

# Stop blinking and showing cursor.
lcd.show_cursor(False)
lcd.blink(False)

print("Stage 5")
# Demo scrolling message right/left.
lcd.clear()
message = 'Scroll'
lcd.message(message)
for i in range(lcd_columns - len(message)):
    sleep(0.5)
    lcd.move_right()
for i in range(lcd_columns - len(message)):
    sleep(0.5)
    lcd.move_left()

print("Stage 6")
# Demo turning backlight off and on.
lcd.clear()
lcd.message('Flash backlight\nin 5 seconds...')
sleep(5.0)
print("Stage 7")
# Turn backlight off.
lcd.set_backlight(0)
sleep(2.0)
print("Stage 8")
# Change message.
lcd.clear()
lcd.message('Goodbye!')
# Turn backlight on.
lcd.set_backlight(1)