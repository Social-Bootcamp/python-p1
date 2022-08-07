import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENTION = 8
SQ_SIZE = HEIGHT // DIMENTION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    """
    Load into a dictionary the pieces images
    """
    pieces = ["wP", "wR", "wN", "wB", "wQ",
              "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load(f"img/{piece}.png"), (SQ_SIZE, SQ_SIZE))


def DrawGameState(screen, gs, validMoves, selected_piece):
    # TODO  add highlight to selected piece and move seggestions
    drawBoard(screen)  # Drawing the board
    drawHighlight(screen, gs, validMoves, selected_piece)
    drawPieces(screen, gs.board)  # Drawing the pieces


def drawHighlight(screen, gs, validMoves, selected_piece):
    if selected_piece != ():
        r, c = selected_piece
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill('blue')
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))

            s.fill("yellow")
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(
                        s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))


def drawBoard(screen):
    """
    Drawing the board squares from left to right
    """
    colors = [p.Color("white"), p.Color("gray")]  # the board colors

    for row in range(DIMENTION):
        for col in range(DIMENTION):
            color = colors[(row+col) % 2]
            p.draw.rect(screen, color, p.Rect(
                col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for row in range(DIMENTION):
        for col in range(DIMENTION):
            piece = board[row][col]
            if piece != "--":  # not empty spot
                screen.blit(IMAGES[piece], p.Rect(
                    col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill("white")
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages()
    running = True

    sqSelected = ()
    playerClickes = []

    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            elif event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClickes = []
                else:
                    sqSelected = (row, col)
                    playerClickes.append(sqSelected)

                if len(playerClickes) == 2:
                    move = ChessEngine.Move(
                        playerClickes[0], playerClickes[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = ()
                        playerClickes = []
                    else:
                        playerClickes = [sqSelected]
                        
            elif event.type == p.KEYDOWN:
                if event.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            print(validMoves)
            moveMade = False

        clock.tick(MAX_FPS)
        DrawGameState(screen, gs, validMoves, sqSelected)
        p.display.flip()


if __name__ == '__main__':
    main()
