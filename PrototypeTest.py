import boardReader as cv
import theboard

# Image output file from camera
imgPath = '...'

# Board Reader library determines current position of chess pieces
cv.read(imgPath)
newPositions = cv.getPositions()

# Board library determines if a valid move has been made and other chess logic
board = theboard.Board()
board.checkMove(newPositions)

# Move was valid
if board.isValidMove:
    print('Valid move')

    # Get necessary info
    currentColor = board.blackorwhite

    startSquare = board.str[0:2]
    endSquare = board.str[2:4]

    # Check for preliminary conditions
    if board.isCheck:
        print('King is in danger')

    elif board.isCheckMate:
        print('King has been captured')

    # Move pieces
    # White move
    elif currentColor == 0:
        print('Move white piece')
        # movePiecesAuto(startSquare, endSquare)

    elif currentColor == 1:
        print('Move black piece')
        # movePiecesAuto(startSquare, endSquare)

# Move was invalid
else:
    print('Invalid move')