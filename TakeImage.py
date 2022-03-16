import subprocess
from PIL import Image
import RPi.GPIO as GPIO



def TakePicture():
    
    # Taking picture
    subprocess.call('fswebcam -r 1280x1280 /home/pi/Desktop/NewImage.jpg', shell=True)


    # Showing the image
    imgPath = '/home/pi/Desktop/NewImage.jpg'  # Specifying path    

    img = Image.open(imgPath)  # Opening image

    img.show()  # Displaying image
    

# Button input

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down= GPIO.PUD_DOWN)

print('program running')

currentState = False
laststate = False

while True:
    lastState = currentState
    if GPIO.input(10) == GPIO.HIGH:
        currentState = True
    else:
        currentState = False
    
    if lastState and not currentState:
        print('Button pushed')
        TakePicture()
    




