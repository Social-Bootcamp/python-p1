
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

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = '--'
            self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        return self.getPossibleMoves()

    def getPossibleMoves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][col][1]
                  
        return moves

    def getPawnMoves(self, row, col, moves):
        color = 'w' if self.whiteToMove else 'b'
        if color == 'w':
            if self.board[row-1][col] == '--':
                moves.append(Move((row,col),(row-1,col),self.board))
                if row == 6 and self.board[row-2][col] == '--':
                    moves.append(Move((row,col),(row-2,col),self.board))
            if col-1 >= 0:
                if self.board[row-1][col-1][0] == 'b':
                    moves.append(Move((row,col),(row-1,col-1),self.board))
            if col+1 <=7:
                if self.board[row-1][col+1][0] == 'b':
                    moves.append(Move((row,col),(row-1,col+1),self.board))
        elif color == 'b':
            if self.board[row+1][col] == '--':
                moves.append(Move((row,col),(row+1,col),self.board))
                if row == 1 and self.board[row+2][col] == '--':
                    moves.append(Move((row,col),(row+2,col),self.board))
            if col-1 >= 0:
                if self.board[row+1][col-1][0] == 'w':
                    moves.append(Move((row,col),(row+1,col-1),self.board))
            if col+1 <=7:
                if self.board[row+1][col+1][0] == 'w':
                    moves.append(Move((row,col),(row+1,col+1),self.board))

    def getBishopMoves(self, row, col, moves):
        bishopMoves = ((1, 1), (1, -1), (-1, -1), (-1, 1))
        color = 'w' if self.whiteToMove else 'b'
        for move in bishopMoves:
            for i in range(1, 8):
                endRow = row + move[0] * i
                endCol = col + move[1] * i

                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endSq = self.board[endRow][endCol]
                    if endSq == '--':
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endSq[0] != color:
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    elif endSq[0] == color:
                        break
                    else:
                        break
                else:
                    break


class Move:
    rankToRows = {"1": 7, "2": 6, "3": 5,
                  "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    filesToCol = {"a": 0, "b": 1, "c": 2,
                  "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

    rowToRanks = dict(map(reversed, rankToRows.items()))
    colToFiles = dict(map(reversed, filesToCol.items()))

    def __init__(self, startSQ, endSQ, board):
        self.startRow = startSQ[0]
        self.startCol = startSQ[1]
        self.endRow = endSQ[0]
        self.endCol = endSQ[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other: object) -> bool:
        if isinstance(other,Move):
            return other.moveID == self.moveID
        return False

    def getChessNotation(self):
        if 'w' in self.pieceMoved:
            return "White: "+self.getRankFile(self.startRow, self.startCol) + " --> " + self.getRankFile(self.endRow, self.endCol)
        return "Black: "+self.getRankFile(self.startRow, self.startCol) + " --> " + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colToFiles[c] + self.rowToRanks[r]

    def __repr__(self) -> str:
        return self.getRankFile(self.endRow, self.endCol)