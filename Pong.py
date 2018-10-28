from flask import Flask, render_template, request
from flask_socketio import SocketIO
import PongGame as PG
import PongSetup as PS
from time import sleep
import threading
import os
import sys

# initialize Flask
app = Flask(__name__)
socketio = SocketIO(app)

if len(sys.argv) > 1:
    game = PS.PongGame()
else:
    game = PG.PongGame()
game_started = False


@app.route('/')
def index():
    """Serve the index HTML"""
    return render_template('index.html')


@socketio.on('connect')
def connect():
    t = threading.Thread(target=run_game)
    t.start()


@socketio.on('keyup')
def keyup(data):
    game.keyup(data['key_code'])
    if data['key_code'] == 81:
        os._exit(0)


@socketio.on('keydown')
def keydown(data):
    game.keydown(data['key_code'])


def run_game():
    global game_started
    if game_started:
        return
    game_started = True
    game.init()
    while True:
        game.tick()
        sleep(.0166667)


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
