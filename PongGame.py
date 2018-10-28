from StepperMotorDriver import StepperMotorDriver as SMD
import math
import RPi.GPIO as GPIO

class PongGame():
    m1 = SMD([21, 16, 12, 25])
    m2 = SMD([26, 27, 13, 5])

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
    HALF_PAD_WIDTH = int(PAD_WIDTH / 2)
    HALF_PAD_HEIGHT = int(PAD_HEIGHT / 2)

    key_States = {40: 0, 38: 0, 83: 0, 87: 0, 73: 0, 74: 0, 75: 0, 76: 0, 81: 0}

    def ball_init(self, right):
        self.ball_position = [int(self.WIDTH / 2), int(self.HEIGHT / 2)]
        horz = 3
        vert = 3
        if not right:
            horz = - horz

        self.ball_velocity = [horz, -vert]
        self.m1.move_to(26.5)
        self.m2.move_to(0)

    def init(self):
        self.paddle1_position = [int(self.HALF_PAD_WIDTH - 1), int(self.HEIGHT / 2)]
        self.paddle2_position = [int(self.WIDTH + 1 - self.HALF_PAD_WIDTH), int(self.HEIGHT / 2)]
        self.right_score = 0
        self.left_score = 0
        self.ball_init(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(19, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)
        self.pwm1 = GPIO.PWM(19, 50)
        self.pwm2 = GPIO.PWM(18, 50)

    def draw(self):
        if self.paddle1_position[1] > self.HALF_PAD_HEIGHT and self.paddle1_position[
            1] < self.HEIGHT - self.HALF_PAD_HEIGHT:
            self.paddle1_position[1] += self.paddle1_vel
        elif self.paddle1_position[1] == self.HALF_PAD_HEIGHT and self.paddle1_vel > 0:
            self.paddle1_position[1] += self.paddle1_vel
        elif self.paddle1_position[1] == self.HEIGHT - self.HALF_PAD_HEIGHT and self.paddle1_vel < 0:
            self.paddle1_position[1] += self.paddle1_vel

        if self.paddle2_position[1] > self.HALF_PAD_HEIGHT and self.paddle2_position[
            1] < self.HEIGHT - self.HALF_PAD_HEIGHT:
            self.paddle2_position[1] += self.paddle2_vel
        elif self.paddle2_position[1] == self.HALF_PAD_HEIGHT and self.paddle2_vel > 0:
            self.paddle2_position[1] += self.paddle2_vel
        elif self.paddle2_position[1] == self.HEIGHT - self.HALF_PAD_HEIGHT and self.paddle2_vel < 0:
            self.paddle2_position[1] += self.paddle2_vel

        self.ball_position[0] += int(self.ball_velocity[0])
        self.ball_position[1] += int(self.ball_velocity[1])

        self.update_laser()
        # sleep(2)
        #
        # self.ball_position[0] = 0
        # self.ball_position[1] = 0
        #
        # self.update_laser()
        # sleep(2)
        #
        # self.ball_position[0] = 0
        # self.ball_position[1] = self.HEIGHT
        #
        # self.update_laser()
        # sleep(2)
        #
        # self.ball_position[0] = self.WIDTH
        # self.ball_position[1] = self.HEIGHT
        #
        # self.update_laser()
        # sleep(2)
        #
        # self.ball_position[0] = self.WIDTH
        # self.ball_position[1] = 0
        #
        # self.update_laser()
        # sleep(5)

        # TODO: Draw Ball!
        # pygame.draw.circle(canvas, RED, ball_position, 20)
        # pygame.draw.polygon(canvas, RED, [[paddle1_position[0] - HALF_PAD_WIDTH, paddle1_position[1] - HALF_PAD_HEIGHT],
        #                                   [paddle1_position[0] - HALF_PAD_WIDTH, paddle1_position[1] + HALF_PAD_HEIGHT],
        #                                   [paddle1_position[0] + HALF_PAD_WIDTH, paddle1_position[1] + HALF_PAD_HEIGHT],
        #                                   [paddle1_position[0] + HALF_PAD_WIDTH, paddle1_position[1] - HALF_PAD_HEIGHT]], 0)
        # pygame.draw.polygon(canvas, RED, [[paddle2_position[0] - HALF_PAD_WIDTH, paddle2_position[1] - HALF_PAD_HEIGHT],
        #                                   [paddle2_position[0] - HALF_PAD_WIDTH, paddle2_position[1] + HALF_PAD_HEIGHT],
        #                                   [paddle2_position[0] + HALF_PAD_WIDTH, paddle2_position[1] + HALF_PAD_HEIGHT],
        #                                   [paddle2_position[0] + HALF_PAD_WIDTH, paddle2_position[1] - HALF_PAD_HEIGHT]], 0)

        if self.ball_position[1] <= self.BALL_RADIUS:
            self.ball_velocity[1] = - self.ball_velocity[1]
        if self.ball_position[1] >= self.HEIGHT + 1 - self.BALL_RADIUS:
            self.ball_velocity[1] = -self.ball_velocity[1]

        if self.ball_position[0] <= self.BALL_RADIUS + self.PAD_WIDTH and self.ball_position[1] in range(
                self.paddle1_position[1] - self.HALF_PAD_HEIGHT, self.paddle1_position[1] + self.HALF_PAD_HEIGHT, 1):
            self.ball_velocity[0] = -self.ball_velocity[0]
            self.ball_velocity[0] *= 1.1
            self.ball_velocity[1] *= 1.1
        elif self.ball_position[0] <= (self.BALL_RADIUS + self.PAD_WIDTH) - 5:
            self.right_score += 1
            self.ball_init(True)

        if self.ball_position[0] >= self.WIDTH + 1 - self.BALL_RADIUS - self.PAD_WIDTH and self.ball_position[
            1] in range(
            self.paddle2_position[1] - self.HALF_PAD_HEIGHT, self.paddle2_position[1] + self.HALF_PAD_HEIGHT, 1):
            self.ball_velocity[0] = -self.ball_velocity[0]
            self.ball_velocity[0] *= 1.1
            self.ball_velocity[1] *= 1.1
        elif self.ball_position[0] >= self.WIDTH + 1 - self.BALL_RADIUS - self.PAD_WIDTH:
            self.left_score += 1
            self.ball_init(False)

    def keydown(self, key):
        self.key_States[key] = 1

    def keyup(self, key):
        self.key_States[key] = 0

    def tick(self):
        self.draw()
        for key in self.key_States.keys():
            if self.key_States[key]:
                if key == 38:
                    self.paddle2_vel = 10
                elif key == 40:
                    self.paddle2_vel = -10
                elif key == 87:
                    self.paddle1_vel = 10
                elif key == 83:
                    self.paddle1_vel = -10
                elif key == 73:
                    #I
                    self.m1.step(2)
                elif key == 75:
                    #K
                    self.m1.step(-2)
                elif key == 74:
                    #J
                    self.m2.step(2)
                elif key == 76:
                    #L
                    self.m2.step(-2)
                elif key == 81:
                    #Q
                    self.m1.cleanup()
            else:
                if not self.key_States[83] and not self.key_States[87]:
                    self.paddle1_vel = 0
                elif not self.key_States[38] and not self.key_States[40]:
                    self.paddle2_vel = 0

    def update_laser(self):
        adjX = (self.ball_position[0] / 40) - 7.5
        adjY = (self.ball_position[1] / 40) + 6
        radius = math.sqrt(math.pow(adjX, 2) + math.pow(adjY, 2))
        theta1 = math.atan2(adjX, adjY) * 180 / math.pi
        theta2 = math.atan2(14, radius) * 180 / math.pi

        self.m2.move_to(theta1)
        self.m1.move_to(theta2)
