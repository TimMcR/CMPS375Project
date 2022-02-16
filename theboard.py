import chess
board = chess.Board()
# 0 is empty, 1 is black, 2 is white
#            [[1, 1, 1, 1, 1, 1, 1, 1 ],
#             [1, 1, 1, 1, 1, 1, 1, 1 ],
#             [0, 0, 0, 0, 0, 0, 0, 0 ],
#             [0, 0, 0, 0, 0, 0, 0, 0 ],
#             [0, 0, 0, 0, 0, 0, 0, 0 ],
#             [0, 0, 0, 0, 0, 0, 0, 0 ],
#             [2, 2, 2, 2, 2, 2, 2, 2 ],
#             [2, 2, 2, 2, 2, 2, 2, 2 ]]


#current = [[1, 1, 1, 1, 1, 1, 1, 1 ],
#           [1, 1, 1, 1, 1, 1, 1, 1 ],
#           [0, 0, 0, 0, 0, 0, 0, 0 ],
#           [0, 0, 0, 0, 0, 0, 0, 0 ],
#           [0, 0, 0, 0, 0, 0, 0, 0 ],
#           [0, 0, 0, 0, 0, 0, 0, 0 ],
#           [2, 2, 2, 2, 2, 2, 2, 2 ],
#           [2, 2, 2, 2, 2, 2, 2, 2 ]]

#nextMove = [[1, 1, 1, 1, 1, 1, 1, 1 ],
#           [1, 1, 1, 1, 1, 1, 1, 1 ],
#           [0, 0, 0, 0, 0, 0, 0, 0 ],
#           [0, 0, 0, 0, 0, 0, 0, 0 ],
#           [0, 0, 0, 0, 0, 2, 0, 0 ],
#           [0, 0, 0, 0, 0, 0, 0, 0 ],
#           [2, 2, 2, 2, 2, 0, 2, 2 ],
#           [2, 2, 2, 2, 2, 2, 2, 2 ]]

#blackcastled = 0
#whitecastled = 0
#blackorwhite = 0 #0 for white, 1 for black







#print(board, "\n")
#print(board.fen(), "\n")

def initBoard():
    return [[1, 1, 1, 1, 1, 1, 1, 1 ],
           [1, 1, 1, 1, 1, 1, 1, 1 ],
           [0, 0, 0, 0, 0, 0, 0, 0 ],
           [0, 0, 0, 0, 0, 0, 0, 0 ],
           [0, 0, 0, 0, 0, 0, 0, 0 ],
           [0, 0, 0, 0, 0, 0, 0, 0 ],
           [2, 2, 2, 2, 2, 2, 2, 2 ],
           [2, 2, 2, 2, 2, 2, 2, 2 ]], "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 ", 0, 0, 0

def checkMove(current, nextMove, boardpattern, blackcastled, whitecastled, blackorwhite):
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
    blackcastlingright = ["e1", "f1", "g1", "h1"]
    blackcastlingleft = ["a1", "b1", "c1", "e1"]
    whitecastlingright = ["e8", "f8", "g8", "h8"]
    whitecastlingleft = ["a8", "b8", "c8", "e8"]
    move1 = "a"
    move2 = "a"
    enpassanttest = "a"
    invalidMove = 0

    for x in range(0,8):
         for y in range(0, 8):
          if nextMove[x][y] != current[x][y]:
              changes.append(ref[x][y])
              placement.append(nextMove[x][y])
              past.append(current[x][y])

    if blackorwhite == 0:
         if len(changes) == 2:
              for x in range(0,2):
                   if placement[x] == 2:
                        move2 = changes[x]
                   else:
                        move1 = changes[x]
              blackorwhite = 1
              str = move1 + move2
              try:
                  board.push_uci(str)
              except:
                  print("invalid move")
                  blackorwhite = 0
                  invalidMove = 1

         elif len(changes)==3:
             for x in range(0, 2):
                 if placement[x] == 2:
                     move2 = changes[x]
                 elif past[x] == 2 and placement[x] == 0:
                     move1 = changes[x]
                 else:
                     enpassanttest = changes[x]

                 if enpassanttest[0:1] == move2[0:1] and enpassanttest[1:2] == move1[1:2]:
                     blackorwhite = 1
                     str = move1 + move2
                     try:
                         board.push_uci(str)
                     except:
                         print("invalid move")
                         blackorwhite = 0
                         invalidMove = 1
                 else:
                     print("invalid move")
                     invalidMove = 1

         elif len(changes)== 4:
              if blackcastlingright == changes and blackcastled == 0:
                  blackorwhite = 1
                  try:
                      board.push_uci("e1g1")
                  except:
                      print("invalid move")
                      blackorwhite = 0
                      invalidMove = 1

              elif blackcastlingleft == changes and blackcastled == 0 and current[7][3] != 0:
                  blackorwhite = 1
                  try:
                      board.push_uci("e1b1")
                  except:
                      print("invalid move")
                      blackorwhite = 0
                      invalidMove = 1
              else:
                  print("Invalid Move")
                  invalidMove = 1
         else:
              print("Invalid Move")
              invalidMove = 1

         if nextMove[7][4] != 2 and invalidMove != 1:
             blackcastled = 1

    else:
         if len(changes) == 2:
              for x in range(0,2):
                   if placement[x] == 1:
                        move2 = changes[x]
                   else:
                        move1 = changes[x]
              blackorwhite = 0
              str = move1 + move2
              try:
                  board.push_uci(str)
              except:
                  print("invalid move")
                  invalidMove = 1
                  blackorwhite = 1

         elif len(changes)==3:
             for x in range(0, 2):
                 if placement[x] == 1:
                     move2 = changes[x]
                 elif past[x] == 1 and placement[x] == 0:
                     move1 = changes[x]
                 else:
                     enpassanttest = changes[x]

                 if enpassanttest[0:1] == move2[0:1] and enpassanttest[1:2] == move1[1:2]:
                     blackorwhite = 0
                     str = move1 + move2
                     try:
                         board.push_uci(str)
                     except:
                         print("invalid move")
                         invalidMove = 1
                         blackorwhite = 1
                 else:
                     print("invalid move")
                     invalidMove = 1

         elif len(changes)== 4:
             if whitecastlingright == changes and whitecastled == 0:
              blackorwhite = 0
              try:
                  board.push_uci("e8g8")
              except:
                  print("invalid move")
                  invalidMove = 1
                  blackorwhite = 1
              print(board, "\n")
             elif whitecastlingleft == changes and whitecastled == 0 and current[1][3] != 0:
              blackorwhite = 0
              try:
                  board.push_uci("e8b8")
              except:
                  print("invalid move")
                  invalidMove = 1
                  blackorwhite = 1
             else:
                 print("Invalid Move")
                 invalidMove = 1

         else:
              print("Invalid Move")
              invalidMove = 1

         if nextMove[1][4] != 2 and invalidMove != 1:
             whitecastled = 1

    return board.fen(), blackcastled, whitecastled, blackorwhite, invalidMove

#print(checkMove(current, nextMove, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 ", blackcastled, whitecastled, blackorwhite))
#legal_moves = list(board.legal_moves)
#print(legal_moves)