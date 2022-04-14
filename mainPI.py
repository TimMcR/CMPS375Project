# main file for Raspberry Pi
# whenever the button is pressed, take a picture of the current board
# then do chess game logic and send the data over to a google sheet

import subprocess
import RPi.GPIO as GPIO
import boardReader as cv
import theboard as brd

board = brd.Board()

# Button input

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print('program running')

currentState = False
lastState = False


def TakePicture():
    imgPath = '/home/cmps-375/CMPS375Project/NewImage.jpg'  # Specifying path

    # Taking picture
    subprocess.call('fswebcam -r 1280x1280 ' + imgPath, shell=True)

    positions = cv.read(imgPath)

    board.checkMove(positions)

    mapper.update(board)


while True:
    lastState = currentState
    if GPIO.input(10) == GPIO.HIGH:
        currentState = True
    else:
        currentState = False

    if lastState and not currentState:
        print('Button pushed')
        TakePicture()
