import pygame as p
import os

from GameState import GameState 



MAX_FPS  = 30
WIDTH, HEIGHT = 640,640
NSQUARE = 8
SQUARE_SIZE = WIDTH//NSQUARE
WHITE = p.Color("white")
BLACK_SQUARE_IMAGE = p.image.load(os.path.join('images','square brown dark.png'))
BLACK_SQUARE = p.transform.scale(BLACK_SQUARE_IMAGE, (SQUARE_SIZE,SQUARE_SIZE))
WHITE_SQUARE_IMAGE = p.image.load(os.path.join('images','square brown light.png'))
WHITE_SQUARE = p.transform.scale(WHITE_SQUARE_IMAGE, (SQUARE_SIZE,SQUARE_SIZE))
GAME_STATE = GameState()

def loadImages():
    pass

def drawBoard(screen):
    pass
    

def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(WHITE)
    running = True
    while running:
        clock.tick(MAX_FPS)
        for e in p.event.get():
            drawBoard(screen)
            if e.type == p.QUIT:
                running = False
        p.display.update()
        
        
if __name__ == "__main__":
    main()