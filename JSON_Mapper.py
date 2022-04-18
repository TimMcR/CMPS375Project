import theboard
import requests
import json

params = dict(
    validMove='True',
    currColor='White',
    startSquare='A1',
    endSquare='B1',
    check='False',
    checkmate='False',
    whiteCastled='False',
    blackCastled='False'
)

url = 'http://10.176.148.111:8000/chessInfo.json'


class Mapper():
    def __int__(self):
        self.prevSquare = ""
        self.data = params

    def update(self, board):
        if board.isValidMove:
            self.data['ValidMove'] = 'True'
        else:
            self.data['ValidMove'] = 'False'

        if board.blackorwhite == 0:
            self.data['currColor'] = 'White'
        else:
            self.data['currColor'] = 'Black'

        self.data['startSquare'] = board.str[0:2]
        self.data['endSquare'] = board.str[2:4]

        if board.isCheck:
            self.data['check'] = 'True'
        else:
            self.data['check'] = 'False'

        if board.isCheckMate:
            self.data['checkmate'] = 'True'
        else:
            self.data['checkmate'] = 'False'

        if board.whitecastled:
            self.data['whiteCastled'] = 'True'
        else:
            self.data['whiteCastled'] = 'False'

        if board.blackcastled:
            self.data['blackCastled'] = 'True'
        else:
            self.data['blackCastled'] = 'False'

        json_object = json.dumps(self.data, indent=4)

        with open("chessInfo.json", "w") as outfile:
            outfile.write(json_object)

    def getData(self):
        resp = requests.get(url=url, params=params)
        self.data = resp.json()

    def isUpdated(self):
        if self.prevSquare != self.data['startSquare']:
            self.prevSquare = self.data['startSquare']
            return True
        else:
            return False

    def getValidMove(self):
        if self.data['validMove'] == 'True':
            return True
        else:
            return False

    def getColor(self):
        return self.data['currColor']

    def getStartSquare(self):
        return self.data['startSquare']

    def getEndSquare(self):
        return self.data['endSquare']

    def getCheck(self):
        if self.data['check'] == 'True':
            return True
        return False

    def getCheckMate(self):
        if self.data['checkmate'] == 'True':
            return True
        return False

    def getWhiteCastled(self):
        if self.data['whiteCastled'] == 'True':
            return True
        return False

    def getBlackCastled(self):
        if self.data['blackCastled'] == 'True':
            return True
        return False
