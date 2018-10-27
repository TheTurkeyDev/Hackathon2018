import spyral //2D game engine

HEIGHT = 1000
WIDTH = 800
GAME_SIZE = (WIDTH, HEIGHT)

class Pong(spyral.Scene) :
    def init(self):
        super(Pong, self).init(GAME_SIZE)
        self.background = spyral.Image(size=GAME_SIZE).fill(0,0,0)