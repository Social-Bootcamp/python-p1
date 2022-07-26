
class GameState:

    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],  # 0
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "bP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]  # 7
        ]
        # Test for checkmate and stalmate
        # self.board = [
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "bK", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["wQ", "--", "wK", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        # ]
        self.whiteToMove = True
        self.moveLog = []
        self.moveFunctions = {'P': self.getPawnMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves,
                              'R': self.getRookMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.CheckMate = False
        self.StalMate = False
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            if move.pieceCaptured != '--':
                self.board[move.startRow][move.startCol] = move.pieceMoved
                self.board[move.endRow][move.endCol] = move.pieceCaptured
            else:
                self.board[move.startRow][move.startCol] = move.pieceMoved
                self.board[move.endRow][move.endCol] = '--'
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
            self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        moves = self.getPossibleMoves()

        for i in range(len(moves)-1,-1,-1):
            self.makeMove(moves[i])

            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                    moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
            if len(moves) == 0 and self.inCheck():
                self.CheckMate = True
                print("checkmate")
            elif len (moves) == 0 and not self.inCheck():
                self.StalMate=True
                print("stalmate")
        return moves

    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squareUnderAttack(self, row, col):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == row and move.endCol == col:
                return True
        return False

    def getPossibleMoves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[row][col][1]
                    self.moveFunctions[piece](row, col, moves)

        return moves

    def getPawnMoves(self, row, col, moves):
        color = 'w' if self.whiteToMove else 'b'
        if color == 'w':
            if self.board[row-1][col] == '--':
                moves.append(Move((row, col), (row-1, col), self.board))
                if row == 6 and self.board[row-2][col] == '--':
                    moves.append(Move((row, col), (row-2, col), self.board))
            if col-1 >= 0:
                if self.board[row-1][col-1][0] == 'b':
                    moves.append(Move((row, col), (row-1, col-1), self.board))
            if col+1 <= 7:
                if self.board[row-1][col+1][0] == 'b':
                    moves.append(Move((row, col), (row-1, col+1), self.board))
        elif color == 'b':
         if (row+1)<8: 
            if self.board[row+1][col] == '--':
                moves.append(Move((row, col), (row+1, col), self.board))
                if row == 1 and self.board[row+2][col] == '--':
                    moves.append(Move((row, col), (row+2, col), self.board))
            if col-1 >= 0:
                if self.board[row+1][col-1][0] == 'w':
                    moves.append(Move((row, col), (row+1, col-1), self.board))
            if col+1 <= 7:
                if self.board[row+1][col+1][0] == 'w':
                    moves.append(Move((row, col), (row+1, col+1), self.board))

    def getKnightMoves(self, row, col, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2),
                       (1, -2), (1, 2), (2, -1), (2, 1))  # move directions
        allyColor = 'w' if self.whiteToMove else 'b'  # ally piece color

        for move in knightMoves:
            endRow = row + move[0]
            endCol = col + move[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endSQ = self.board[endRow][endCol]
                if endSQ[0] != allyColor:
                    moves.append(
                        Move((row, col), (endRow, endCol), self.board))

    def getRookMoves(self, row, col, moves):
        directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        enemyColor = 'b' if self.whiteToMove else 'w'

        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i

                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endSQ = self.board[endRow][endCol]
                    if endSQ == '--':
                        moves.append(
                            Move((row, col), (endRow, endCol), self.board))
                    elif endSQ[0] == enemyColor:
                        moves.append(
                            Move((row, col), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self, row, col, moves):
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1),
                      (1, 1), (-1, 1), (1, -1), (-1, -1))
        enemyColor = 'b' if self.whiteToMove else 'w'

        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i

                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endSQ = self.board[endRow][endCol]
                    if endSQ == '--':
                        moves.append(
                            Move((row, col), (endRow, endCol), self.board))
                    elif endSQ[0] == enemyColor:
                        moves.append(
                            Move((row, col), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKingMoves(self, row, col, moves):

        kingMoves = ((1, 0), (-1, 0), (0, 1), (0, -1),
                     (1, 1), (-1, 1), (1, -1), (-1, -1))
        allyColor = 'w' if self.whiteToMove else 'b'

        for i in kingMoves:

            endRow = row + i[0]
            endCol = col + i[1]

            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endSQ = self.board[endRow][endCol]
                if endSQ[0] != allyColor:
                    moves.append(
                        Move((row, col), (endRow, endCol), self.board))

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
                        moves.append(
                            Move((row, col), (endRow, endCol), self.board))
                    elif endSq[0] != color:
                        moves.append(
                            Move((row, col), (endRow, endCol), self.board))
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
        self.moveID = self.startRow * 1000 + self.startCol * \
            100 + self.endRow * 10 + self.endCol

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Move):
            return other.moveID == self.moveID
        return False

    def getChessNotation(self):
        if self.pieceMoved[1] != 'P':
            if 'w' in self.pieceMoved:
                return "White: " + self.pieceMoved[1]+self.getRankFile(self.endRow, self.endCol)
            return "Black: " + self.pieceMoved[1] + self.getRankFile(self.endRow, self.endCol)
        else:
            if 'w' in self.pieceMoved:
                return "White: " + self.getRankFile(self.endRow, self.endCol)
            return "Black: " + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colToFiles[c] + self.rowToRanks[r]

    def __repr__(self) -> str:
        return self.getRankFile(self.endRow, self.endCol)
