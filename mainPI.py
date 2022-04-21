# main file for Raspberry Pi
# whenever the button is pressed, take a picture of the current board
# then do the chess game logic and send the data over to a google sheet

import subprocess
import RPi.GPIO as GPIO
import boardReader as cv
import theboard as brd
import JSON_Mapper as j

# Status of current chess board
board = brd.Board()

# Create data mapper to write to the JSON file from the PI
# Make sure url is correct before running
url = 'http://192.168.1.23:8000/chessInfo.json'
mapper = j.Mapper()
mapper.setURL(url)

# Button input
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print('program running')

currentState = False
lastState = False


# When the button is pushed, take a picture, read the chess board, and upadte the JSON file
def TakePicture():
    # Specifying path
    imgPath = '/home/cmps-375/CMPS375Project/NewImage.jpg'

    # Take picture
    subprocess.call('fswebcam -r 1280x1280 ' + imgPath, shell=True)

    # Read positions of chess pieces
    positions = cv.read(imgPath)

    # Validate the chess move
    board.checkMove(positions)

    # Update the JSON file on the PI
    mapper.update(board)


# Main loop
while True:
    lastState = currentState
    if GPIO.input(10) == GPIO.HIGH:
        currentState = True
    else:
        currentState = False

    # Run when the button is toggled
    if lastState and not currentState:
        print('Button pushed')
        TakePicture()