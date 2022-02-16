import unittest
#Rename to actual library names
import theboard

#TODO add custom libraries to project and write enough code to pass unit tests

class MyTestCase(unittest.TestCase):
    def test_checkMove(self):
        c = theboard
        self.assertEqual(c.checkMove(
           [[1, 1, 1, 1, 1, 1, 1, 1 ],
           [1, 1, 1, 1, 1, 1, 1, 1 ],
           [0, 0, 0, 0, 0, 0, 0, 0 ],
           [0, 0, 0, 0, 0, 0, 0, 0 ],
           [0, 0, 0, 0, 0, 0, 0, 0 ],
           [0, 0, 0, 0, 0, 0, 0, 0 ],
           [2, 2, 2, 2, 2, 2, 2, 2 ],
           [2, 2, 2, 2, 2, 2, 2, 2 ]],

           [[1, 1, 1, 1, 1, 1, 1, 1 ],
           [1, 1, 1, 1, 1, 1, 1, 1 ],
           [0, 0, 0, 0, 0, 0, 0, 0 ],
           [0, 0, 0, 0, 0, 0, 0, 0 ],
           [0, 0, 0, 0, 0, 2, 0, 0 ],
           [0, 0, 0, 0, 0, 0, 0, 0 ],
           [2, 2, 2, 2, 2, 0, 2, 2 ],
           [2, 2, 2, 2, 2, 2, 2, 2 ]],

           "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 ", 0, 0, 0),
           ('rnbqkbnr/pppppppp/8/8/5P2/8/PPPPP1PP/RNBQKBNR b KQkq - 0 1', 0, 0, 1, 0))

        self.assertEqual(c.checkMove(
           [[1, 1, 1, 1, 1, 1, 1, 1 ],
           [1, 1, 1, 1, 1, 1, 1, 1 ],
           [0, 0, 0, 0, 0, 0, 0, 0 ],
           [0, 0, 0, 0, 0, 0, 0, 0 ],
           [0, 0, 0, 0, 0, 0, 0, 0 ],
           [0, 0, 0, 0, 0, 2, 2, 0 ],
           [2, 2, 2, 2, 2, 2, 2, 2 ],
           [2, 2, 2, 2, 2, 0, 0, 2 ]],

           [[1, 1, 1, 1, 1, 1, 1, 1 ],
           [1, 1, 1, 1, 1, 1, 1, 1 ],
           [0, 0, 0, 0, 0, 0, 0, 0 ],
           [0, 0, 0, 0, 0, 0, 0, 0 ],
           [0, 0, 0, 0, 0, 0, 0, 0 ],
           [0, 0, 0, 0, 0, 2, 2, 0 ],
           [2, 2, 2, 2, 2, 2, 2, 2 ],
           [2, 2, 2, 2, 0, 2, 2, 0 ]],

           "rnbqkbnr/pppppppp/8/8/8/5BN1/PPPPPPPP/RNBQK2R w KQkq - 0 1 ", 0, 0, 0),
           ('rnbqkbnr/pppppppp/8/8/8/5BN1/PPPPPPPP/RNBQ1RK1 b kq - 1 1', 1, 0, 1, 0))

        self.assertEqual(c.checkMove(
           [[1, 1, 1, 1, 1, 1, 1, 1 ],
           [1, 1, 1, 1, 1, 1, 1, 1 ],
           [0, 0, 0, 0, 0, 0, 0, 0 ],
           [0, 0, 0, 0, 0, 0, 0, 0 ],
           [0, 0, 0, 0, 0, 0, 0, 0 ],
           [0, 0, 0, 0, 0, 0, 0, 0 ],
           [2, 2, 2, 2, 2, 2, 2, 2 ],
           [2, 2, 2, 2, 2, 2, 2, 2 ]],

           [[1, 1, 1, 1, 1, 1, 1, 1 ],
           [1, 1, 1, 1, 1, 1, 1, 1 ],
           [0, 0, 0, 0, 0, 0, 0, 0 ],
           [0, 0, 0, 0, 0, 2, 0, 0 ],
           [0, 0, 0, 0, 0, 0, 0, 0 ],
           [0, 0, 0, 0, 0, 0, 0, 0 ],
           [2, 2, 2, 2, 2, 0, 2, 2 ],
           [2, 2, 2, 2, 2, 2, 2, 2 ]],

           "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 ", 0, 0, 0),
           ('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 0, 0, 0, 1))

        self.assertEqual(c.initBoard(), (
           [[1, 1, 1, 1, 1, 1, 1, 1 ],
           [1, 1, 1, 1, 1, 1, 1, 1 ],
           [0, 0, 0, 0, 0, 0, 0, 0 ],
           [0, 0, 0, 0, 0, 0, 0, 0 ],
           [0, 0, 0, 0, 0, 0, 0, 0 ],
           [0, 0, 0, 0, 0, 0, 0, 0 ],
           [2, 2, 2, 2, 2, 2, 2, 2 ],
           [2, 2, 2, 2, 2, 2, 2, 2 ]],

           "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 ", 0, 0, 0))


if __name__ == '__main__':
    unittest.main()