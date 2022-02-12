import unittest
#Rename to actual library names
import ChessTracker
import BoardVision

#TODO add custom libraries to project and write enough code to pass unit tests

class MyTestCase(unittest.TestCase):
    def test_ChessTracker(self):
        c = ChessTracker()
        #Create a new chess board for future validation
        c.initBoard()

    def test_boardVision(self):
        v = BoardVision()
        #Take a picture of the board with no pieces on it
        v.initClearBoard()


if __name__ == '__main__':
    unittest.main()