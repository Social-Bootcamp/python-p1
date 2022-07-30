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


def DrawGameState(screen, gs):
    # TODO  add highlight to selected piece and move seggestions
    drawBoard(screen)  # Drawing the board
    drawPieces(screen, gs.board)  # Drawing the pieces


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
    loadImages()
    running = True

    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
        clock.tick(MAX_FPS)
        DrawGameState(screen, gs)
        p.display.flip()


if __name__ == '__main__':
    main()
