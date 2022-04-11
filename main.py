# TODO import other libraries when ready
# TODO set up push-button to toggle game pause

# Import libraries for GPIO and USB Camera
import subprocess
from PIL import Image
#import RPi.GPIO as GPIO

import ChessEngine as eng
import theboard as brd
#import boardReader as cv

# Create new instance of the chess game
game = eng.ChessGame()
board = brd.Board()

# Assign the button to pin 10
# Un-comment when running on pi
#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(10, GPIO.IN, pull_up_down= GPIO.PUD_DOWN)

# If we want to load the videos then run setUpMenuWait then setupVideos
# Otherwise just load setupMenuReady

def setupVideos():
    game.setupMenuWait()
    game.setupVideos()

def setupNoVideos():
    game.setupMenuReady()

def runGameWithCamera():
    currentButtonState = False

    # Main game loop
    while True:
        # If the button is pressed
        lastButtonState = currentButtonState
        #if GPIO.input(10) == GPIO.HIGH:
        #    currentButtonState = True
        #else:
        #    currentButtonState = False

        toggle = lastButtonState and not currentButtonState

        if toggle:
            # Take picture
            imgPath = '/home/pi/Desktop/NewImage.jpg'
            subprocess.call('fswebcam -r 1280x1280 ' + imgPath, shell=True)

            # Send picture to opencv and determine piece positions
            positions = cv.read()

            # Send positions to board library
            board.checkMove(positions)

            if board.invalidmove == 0:
                # If move is valid then move pieces
                print("Move was valid, proceed")

                # Piece move code to write
                # If a castling move was made, move both rook and king

                # Toggle color
                game.toggleColor()
            else:
                # If move is invalid try again
                print("Move was invalid, try again")

            #game.movePieceAuto("a1", "a3")

        game.step()

def runGameWithMouse():
    game.run()

# Main game code
setupNoVideos()
runGameWithMouse()