import boardReader as cv
import theboard

# Image output from camera
imgPath = '...'

# Board Reader library determines current position of chess pieces
cv.read(imgPath)
newPositions = cv.getPositions()

# Board library determines if a valid move has been made and other chess logic
board = theboard.Board()
board.checkMove(newPositions)
if board.isValidMove:
    print('Valid move')
    currentColor = board.blackorwhite
    # Check for preliminary conditions
    if board.isCheck:
        print('King is in danger')

    if board.isCheckMate:
        print('King has been captured')
    else:
        # Move pieces
        if currentColor == 0 and board.whitecastled:
            print('White has castled')
        if currentColor == 1 and board.blackcastled:
            print('Black has castled')


else:
    print('Invalid move')