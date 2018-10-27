import Adafruit_CharLCD as LCD
from time import sleep
import pygame, sys
from pygame.locals import *

lcd_rs = 27  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en = 22
lcd_d4 = 25
lcd_d5 = 24
lcd_d6 = 23
lcd_d7 = 18
lcd_backlight = 4
lcd_columns = 16
lcd_rows = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

# Print a two line message
lcd.message('Hello\nworld!')

# Wait 5 seconds
sleep(5.0)

# Demo showing the cursor.
lcd.clear()
lcd.show_cursor(True)
lcd.message('Show cursor')

sleep(5.0)

# Demo showing the blinking cursor.
lcd.clear()
lcd.blink(True)
lcd.message('Blink cursor')

sleep(5.0)

# Stop blinking and showing cursor.
lcd.show_cursor(False)
lcd.blink(False)

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

# Demo turning backlight off and on.
lcd.clear()
lcd.message('Flash backlight\nin 5 seconds...')
sleep(5.0)
# Turn backlight off.
lcd.set_backlight(0)
sleep(2.0)
# Change message.
lcd.clear()
lcd.message('Goodbye!')
# Turn backlight on.
lcd.set_backlight(1)

pygame.init()

ball_position = [0, 0]
ball_velocity = [0, 0]
paddle1_vel = 0
paddle2_vel = 0
left_score = 0
right_score = 0
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Pong')


def ball_init(right):
    global ball_position, ball_velocity
    ball_position = [WIDTH / 2, HEIGHT / 2]
    horz = 3
    vert = 3
    if right == False:
        horz = - horz

    ball_velocity = [horz, -vert]


def init():
    global paddle1_position, paddle2_position, paddle1_vel, paddle2_vel, left_score, right_score
    paddle1_position = [HALF_PAD_WIDTH - 1, HEIGHT / 2]
    paddle2_position = [WIDTH + 1 - HALF_PAD_WIDTH, HEIGHT / 2]
    right_score = 0
    left_score = 0
    ball_init(False)


def draw(canvas):
    global paddle1_position, paddle2_position, ball_position, ball_velocity, left_score, right_score

    canvas.fill(BLACK)

    if paddle1_position[1] > HALF_PAD_HEIGHT and paddle1_position[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle1_position[1] += paddle1_vel
    elif paddle1_position[1] == HALF_PAD_HEIGHT and paddle1_vel > 0:
        paddle1_position[1] += paddle1_vel
    elif paddle1_position[1] == HEIGHT - HALF_PAD_HEIGHT and paddle1_vel < 0:
        paddle1_position[1] += paddle1_vel

    if paddle2_position[1] > HALF_PAD_HEIGHT and paddle2_position[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle2_position[1] += paddle2_vel
    elif paddle2_position[1] == HALF_PAD_HEIGHT and paddle2_vel > 0:
        paddle2_position[1] += paddle2_vel
    elif paddle2_position[1] == HEIGHT - HALF_PAD_HEIGHT and paddle2_vel < 0:
        paddle2_position[1] += paddle2_vel

    ball_position[0] += int(ball_velocity[0])
    ball_position[1] += int(ball_velocity[1])

    pygame.draw.circle(canvas, RED, ball_position, 20, 0)
    pygame.draw.polygon(canvas, RED, [[paddle1_position[0] - HALF_PAD_WIDTH, paddle1_position[1] - HALF_PAD_HEIGHT],
                                      [paddle1_position[0] - HALF_PAD_WIDTH, paddle1_position[1] + HALF_PAD_HEIGHT],
                                      [paddle1_position[0] + HALF_PAD_WIDTH, paddle1_position[1] + HALF_PAD_HEIGHT],
                                      [paddle1_position[0] + HALF_PAD_WIDTH, paddle1_position[1] - HALF_PAD_HEIGHT]], 0)
    pygame.draw.polygon(canvas, RED, [[paddle2_position[0] - HALF_PAD_WIDTH, paddle2_position[1] - HALF_PAD_HEIGHT],
                                      [paddle2_position[0] - HALF_PAD_WIDTH, paddle2_position[1] + HALF_PAD_HEIGHT],
                                      [paddle2_position[0] + HALF_PAD_WIDTH, paddle2_position[1] + HALF_PAD_HEIGHT],
                                      [paddle2_position[0] + HALF_PAD_WIDTH, paddle2_position[1] - HALF_PAD_HEIGHT]], 0)

    if int(ball_position[1]) <= BALL_RADIUS:
        ball_velocity[1] = - ball_velocity[1]
    if int(ball_position[1]) >= HEIGHT + 1 - BALL_RADIUS:
        ball_velocity[1] = -ball_velocity[1]

    if int(ball_position[0]) <= BALL_RADIUS + PAD_WIDTH and int(ball_position[1]) in range(
            paddle1_position[1] - HALF_PAD_HEIGHT, paddle1_position[1] + HALF_PAD_HEIGHT, 1):
        ball_velocity[0] = -ball_velocity[0]
        ball_velocity[0] *= 1.1
        ball_velocity[1] *= 1.1
    elif int(ball_position[0]) <= BALL_RADIUS + PAD_WIDTH:
        right_score += 1
        ball_init(True)

    if int(ball_position[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and int(ball_position[1]) in range(
            paddle2_position[1] - HALF_PAD_HEIGHT, paddle2_position[1] + HALF_PAD_HEIGHT, 1):
        ball_velocity[0] = -ball_velocity[0]
        ball_velocity[0] *= 1.1
        ball_velocity[1] *= 1.1
    elif int(ball_position[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
        left_score += 1
        ball_init(False)

    font = pygame.font.SysFont("Times New Roman", 20)
    leftScore = font.render("Left " + str(left_score), 1, (255, 0, 0))
    canvas.blit(leftScore, (50, 350))

    rightScore = font.render("Right " + str(right_score), 1, (255, 0, 0))
    canvas.blit(rightScore, (480, 350))


def keydown(event):
    global paddle1_vel, paddle2_vel

    if event.key == K_UP:
        paddle2_vel = -10
    elif event.key == K_DOWN:
        paddle2_vel = 10
    elif event.key == K_w:
        paddle1_vel = -10
    elif event.key == K_s:
        paddle1_vel = 10


def keyup(event):
    global paddle1_vel, paddle2_vel

    if event.key in (K_w, K_s):
        paddle1_vel = 0
    elif event.key in (K_UP, K_DOWN):
        paddle2_vel = 0


init()

while True:

    draw(window)

    for event in pygame.event.get():

        if event.type == KEYUP:
            keyup(event)
        elif event.type == KEYDOWN:
            keydown(event)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
