import theboard
import requests
import json

params = dict(
    validMove=True,
    currColor='White',
    startSquare='A1',
    endSquare='B1',
    check=False,
    checkmate=False,
    whiteCastled=False,
    blackCastled=False
)


class Mapper():
    def __int__(self, newURL):
        self.prevSquare = ""
        self.data = params

    def setURL(self, newURL):
        self.url = newURL

    def update(self, board):
        self.data['ValidMove'] = board.isValidMove

        if board.blackorwhite == 0:
            self.data['currColor'] = 'White'
        else:
            self.data['currColor'] = 'Black'

        self.data['startSquare'] = board.str[0:2]
        self.data['endSquare'] = board.str[2:4]

        self.data['check'] = board.isCheck

        self.data['checkmate'] = board.isCheckMate

        self.data['whiteCastled'] = board.whitecastled

        self.data['blackCastled'] = board.blackcastled

        json_object = json.dumps(self.data, indent=4)

        with open("chessInfo.json", "w") as outfile:
            outfile.write(json_object)

    def getData(self):
        resp = requests.get(url=self.url, params=params)
        self.data = resp.json()

    def isUpdated(self):
        if self.prevSquare != self.data['startSquare']:
            self.prevSquare = self.data['startSquare']
            return True
        else:
            return False

    def getValidMove(self):
        return self.data['validMove']

    def getColor(self):
        return self.data['currColor']

    def getStartSquare(self):
        return self.data['startSquare']

    def getEndSquare(self):
        return self.data['endSquare']

    def getCheck(self):
        return self.data['check']

    def getCheckMate(self):
        return self.data['checkmate']

    def getWhiteCastled(self):
        return self.data['whiteCastled']

    def getBlackCastled(self):
        return self.data['blackCastled']