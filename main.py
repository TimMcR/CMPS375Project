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
    game.run()

def runNoVideos():
    game.setupMenuReady()
    game.run()

runVideos()
#runNoVideos()