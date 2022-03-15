# TODO import other libraries when ready
# TODO set up push-button to toggle game pause

import ChessEngine as eng

# Create new instance of the chess game
game = eng.ChessGame()

# If we want to load the videos then run setUpMenuWait then setupVideos
# Otherwise just load setupMenuReady

def runVideos():
    game.setupMenuWait()
    game.setupVideos()
    #game.run()

def runNoVideos():
    game.setupMenuReady()
    #game.run()

#runVideos()
runNoVideos()

while True:
    #if buttonPressed:
        #take picture
        #send picture to opencv
        #determine piece positions
        #send positions to board library
        #if move was valid, detect pieces moved and move them
        #then toggle color

        #game.movePieceAuto("a1", "a3")
        #game.toggleColor()

    game.step()

# Example to move a piece:
# game.movePieceAuto("a1", "a3")