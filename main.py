# TODO import other libraries when ready
# TODO set up bluetooth serial connection

# Create new instance of the chess game
import ChessEngine as eng
game = eng.ChessGame()

# If we want to load the videos then run setUpMenuWait then setupVideos
# Otherwise just load setupMenuReady

def setupVideos():
    game.setupMenuWait()
    game.setupVideos()

def setupNoVideos():
    game.setupMenuReady()

# method is running with old unusable logic
def runGameWithCamera():
    # Main game loop
    while True:
        if mapper.updated():
            if mapper.getValidMove():
                # If move is valid then move pieces
                print("Move was valid, proceed")

                currentColor = mapper.getColor()
                startSquare = mapper.getStartSquare()
                endSquare = mapper.getEndSquare()

                # Check for preliminary conditions
                if mapper.getCheck():
                    print('King is in danger')
                    game.setAlarmLightOn()

                else:
                    game.setAlarmLightOff()

                if mapper.getCheckMate():
                    print('King has been captured')
                    game.movePieceCheckmateAuto(startSquare, endSquare)

                else:
                    # White has made a move
                    if currentColor == 'White':
                        if mapper.getWhiteCastled():
                            game.movePieceWhiteCastle(startSquare, endSquare)
                        else:
                            game.movePieceAuto(startSquare, endSquare)

                    # Black has made a move
                    else:
                        if mapper.getBlackCastled():
                            game.movePieceCheckmateAuto(startSquare, endSquare)
                        else:
                            game.movePieceAuto(startSquare, endSquare)

                # Toggle color
                game.toggleColor()
            else:
                # If move is invalid try again
                print("Move was invalid, try again")

        game.step()

def runGameWithMouse():
    game.run()

# Main game code
setupNoVideos()
runGameWithMouse()