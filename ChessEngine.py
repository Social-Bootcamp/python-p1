
class GameState:

    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self,move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

class Move:

    rankToRows = {"1": 7, "2": 6, "3": 5,
                  "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    filesToCol = {"a": 0, "b": 1, "c": 2,
                  "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

    rowToRanks = {val:key for key,val in rankToRows.items()}
    colToFiles = {val:key for key,val in filesToCol.items()}


    def __init__(self, startSQ, endSQ, board):
        self.startRow = startSQ[0]
        self.startCol = startSQ[1]
        self.endRow = endSQ[0]
        self.endCol = endSQ[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]


    def getChessNotation(self):
        if 'w' in self.pieceMoved:
            return "White: "+self.getRankFile(self.startRow,self.startCol) +" --> "+ self.getRankFile(self.endRow, self.endCol)
        return "Black: "+self.getRankFile(self.startRow,self.startCol) +" --> "+ self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self,r,c):
        return self.colToFiles[c] + self.rowToRanks[r]