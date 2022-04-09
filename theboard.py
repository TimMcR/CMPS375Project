import chess
board = chess.Board()

#board.fen() is the state of the board used by the chess library, you will probably not need this

#blackcastled and whitecastled:
#0 means the king has not moved and has the ability to castle
#1 means the king has moved regardless of castling or not, losing the ability to castle in the future

#blackorwhite: determines whose turn it is. 0 for white and 1 for black

#invalidMove: 0 if the move is valid, 1 if it is not

#captured: the captured piece if there is one
#this will be in the form of a single letter representing the piece. uppercase for white and lowercase for black

#capturee: the piece that captures if there is one
#same rules as captured

#checks: an array containing strings of the piece letter and board square combined
#letter portion follows the same rules as captured

#str: this is the move that is done formatted as squareonesquaretwo
#changed this so it always displays "no detectable move" if it's invalid

#outcome: this will display "none" if the game hasn't ended yet
#if the game has ended then it will be displayed in this format:
#Outcome(termination=<Termination.[reason for game ending]: 1>, winner(whoever's turn it currently is)=[True or False])

#moveexport: gives the array that will be put into the next run of the function for current

# From Ramsey: I just put everything into an object and made the outputs into instance variables

class Board():

    def initBoard(self):

        self.blackcastled = 0
        self.whitecastled = 0
        self.blackorwhite = 0
        self.invalidmove = 0

        return [[1, 1, 1, 1, 1, 1, 1, 1 ],
               [1, 1, 1, 1, 1, 1, 1, 1 ],
               [0, 0, 0, 0, 0, 0, 0, 0 ],
               [0, 0, 0, 0, 0, 0, 0, 0 ],
               [0, 0, 0, 0, 0, 0, 0, 0 ],
               [0, 0, 0, 0, 0, 0, 0, 0 ],
               [2, 2, 2, 2, 2, 2, 2, 2 ],
               [2, 2, 2, 2, 2, 2, 2, 2 ]], "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 ", 0, 0, 0


    def checkMove(self, current, nextMove, boardpattern, blackcastled, whitecastled, blackorwhite):
        board = chess.Board(boardpattern)
        ref = [["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8" ],
               ["a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7" ],
               ["a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6" ],
               ["a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5" ],
               ["a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4" ],
               ["a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3" ],
               ["a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2" ],
               ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1" ]]

        changes = []
        placement = []
        past = []
        possiblecaptures = []
        move1 = "a"
        move2 = "a"
        enpassanttest = "a"
        invalidMove = 0
        edited = ""
        captured = "none"
        capturee = "none"
        checks = []
        if blackorwhite == 0:
            play = 0
            next = 1
            player = 2
            opponent = 1
            playercastled = whitecastled
            playercastleleft = ["a1", "b1", "c1", "e1"]
            playercastleright = ["e1", "f1", "g1", "h1"]
            kingstart = 7
            castleright = "e1g1"
            castleleft = "e1b1"
        else:
            play = 1
            next = 0
            player = 1
            opponent = 2
            playercastled = blackcastled
            playercastleleft = ["a8", "b8", "c8", "e8"]
            playercastleright = ["e8", "f8", "g8", "h8"]
            kingstart = 0
            castleright = "e8g8"
            castleleft = "e8b8"

        array = [["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"],
                 ["a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"],
                 ["a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6"],
                 ["a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5"],
                 ["a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4"],
                 ["a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3"],
                 ["a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"],
                 ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"]]

        for w in range(0, len(boardpattern)):
            if boardpattern[w:w + 1] != "/":
                if boardpattern[w:w + 1] == " ":
                    break
                try:
                    for x in range(0, int(boardpattern[w:w + 1])):
                        edited = edited + "0"
                except:
                    edited = edited + boardpattern[w:w + 1]

        for i in range(0, 8):
            for j in range(0, 8):
                array[i][j] = edited[i * 8 + j:i * 8 + j + 1]

        for x in range(0,8):
             for y in range(0, 8):
              if nextMove[x][y] != current[x][y]:
                  changes.append(ref[x][y])
                  placement.append(nextMove[x][y])
                  past.append(current[x][y])
                  possiblecaptures.append(array[x][y])

        if len(changes) == 2:
              for x in range(0,2):
                   if placement[x] == player:
                        move2 = changes[x]
                   else:
                        move1 = changes[x]
                   if past[x] == opponent and placement[x] == player:
                       captured = possiblecaptures[x]
                       possiblecaptures.remove(captured)
                       capturee = possiblecaptures[0]
              blackorwhite = next
              str = move1 + move2
              try:
                  board.push_uci(str)
              except:
                  str = "no detectable move"
                  print("invalid move")
                  blackorwhite = play
                  invalidMove = 1
                  captured = "none"
                  capturee = "none"

        elif len(changes)==3:
             for x in range(0, 3):
                 if placement[x] == player:
                     move2 = changes[x]
                 elif past[x] == player and placement[x] == 0:
                     move1 = changes[x]
                 else:
                     enpassanttest = changes[x]

             if play == 0:
                 capturee = "P"
                 captured = "p"
             else:
                 capturee = "p"
                 captured = "P"

             if enpassanttest[0:1] == move2[0:1] and enpassanttest[1:2] == move1[1:2]:
                 blackorwhite = next
                 str = move1 + move2
                 try:
                     board.push_uci(str)
                 except:
                     str = "no detectable move"
                     print("invalid move")
                     blackorwhite = play
                     invalidMove = 1
                     captured = "none"
                     capturee = "none"
             else:
                str = "no detectable move"
                print("invalid move")
                invalidMove = 1
                captured = "none"
                capturee = "none"

        elif len(changes)== 4:
              if playercastleright == changes and playercastled == 0:
                  blackorwhite = next
                  try:
                      str = castleright
                      board.push_uci(castleright)
                  except:
                      str = "no detectable move"
                      print("invalid move")
                      blackorwhite = play
                      invalidMove = 1

              elif playercastleleft == changes and playercastled == 0 and current[kingstart][4] != 0:
                  blackorwhite = next
                  try:
                      str = castleleft
                      board.push_uci(castleleft)
                  except:
                      str = "no detectable move"
                      print("invalid move")
                      blackorwhite = play
                      invalidMove = 1
              else:
                  str = "no detectable move"
                  print("Invalid Move")
                  invalidMove = 1
        else:
              str = "no detectable move"
              print("Invalid Move")
              invalidMove = 1

        if board.king(chess.BLACK) != 60:
            blackcastled = 1
        if board.king(chess.WHITE) != 4:
            whitecastled = 1

        if board.is_check() == True:
            count = 0
            if blackorwhite == 0:
                attackers = board.attackers(chess.BLACK, board.king(chess.WHITE))
            else:
                attackers = board.attackers(chess.WHITE, board.king(chess.BLACK))
            for square in attackers:
                print(array[int(7 - ((square - (square % 8)) / 8))][square % 8])
                checks[count] = array[int(7 - ((square - (square % 8)) / 8))][square % 8] + ref[int(7 - ((square - (square % 8)) / 8))][square % 8]
                count += 1

        outcome = "None"
        if bool(board.is_game_over()) == True:
            outcome = board.outcome()

        if invalidMove == 1:
            moveexport = current
        else:
            moveexport = nextMove

        self.blackcastled = blackcastled
        self.whitecastled = whitecastled
        self.blackorwhite = blackorwhite
        self.invalidmove = invalidMove

        self.captured = captured
        self.capturee = capturee
        self.checks = checks
        self.str = str
        self.outcome = outcome
        self.moveexport = moveexport

        return board.fen(), blackcastled, whitecastled, blackorwhite, invalidMove, captured, capturee, checks, str, outcome, moveexport


