import ChessEngine as eng
import JSON_Mapper as j

# Create new instance of the chess game
game = eng.ChessGame()

# Create data mapper to write to the JSON file from the PI
# Make sure url is correct before running
url = 'http://192.168.1.23:8000/chessInfo.json'
mapper = j.Mapper()
mapper.setURL(url)

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
        mapper.getData()
        if mapper.isUpdated():
            if mapper.getValidMove():
                # If move is valid then move pieces
                print('Move was valid, proceed')

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
                    if currentColor == 'White':
                        game.showWhiteWinScreen()
                    else:
                        game.showBlackWinScreen()

                else:
                    # White has made a move
                    if currentColor == 'White':
                        if mapper.getWhiteCastled():
                            print('White King has castled')
                            game.movePieceWhiteCastle(startSquare, endSquare)
                        else:
                            print('White has moved')
                            game.movePieceAuto(startSquare, endSquare)

                    # Black has made a move
                    else:
                        if mapper.getBlackCastled():
                            print('Black King has castled')
                            game.movePieceCheckmateAuto(startSquare, endSquare)
                        else:
                            print('Black has moved')
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
