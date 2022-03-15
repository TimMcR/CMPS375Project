# TODO import other libraries when ready
# TODO set up push-button to toggle game pause

import ChessEngine as eng

# Create new instance of the chess game
game = eng.ChessGame()

# If we want to load the videos then run setUpMenuWait then setupVideos
# Otherwise just load setupMenuReady

def setupVideos():
    game.setupMenuWait()
    game.setupVideos()
    #game.run()

def setupNoVideos():
    game.setupMenuReady()
    #game.run()

def runGameWithCamera():
    while True:
        #if buttonPressed:
            #take picture
            #send picture to opencv
            #determine piece positions
            #send positions to board library
            #if move was valid, move pieces
            #if a castling move was made, move both rook and king
            #then toggle color

            #game.movePieceAuto("a1", "a3")
            #game.toggleColor()

        game.step()

def runGameWithMouse():
    game.run()

# Main game code
setupVideos()
runGameWithMouse()