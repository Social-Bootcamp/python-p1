import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENTION = 8
SQ_SIZE = HEIGHT // DIMENTION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ["wP","wR","wN","wB","wQ","wK","bP","bR","bN","bB","bQ","bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f"img/{piece}.png"), (SQ_SIZE,SQ_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill("white")
    gs = ChessEngine.GameState()
    loadImages()
    running = True

    while  running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
        clock.tick(MAX_FPS)
        p.display.flip()

if __name__ == '__main__':
    main()
