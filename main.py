
from re import S
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
IMAGES = {}

def loadImages():
    pieces = ['br','bk','bb','bq','bc','bp','wr','wk','wb','wq','wc','wp']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(os.path.join('images',piece+'.png')),(SQUARE_SIZE,SQUARE_SIZE))
 
def drawBoard(screen):

    rect = p.Rect(0,0,SQUARE_SIZE,SQUARE_SIZE)
    board = GAME_STATE.board
    for row in range(NSQUARE):
        for column in range(NSQUARE):
            if (column + row) %2 == 0:
                screen.blit(BLACK_SQUARE,(column*SQUARE_SIZE,row*SQUARE_SIZE))
            else:
                screen.blit(WHITE_SQUARE,(column*SQUARE_SIZE,row*SQUARE_SIZE))
            if board[row][column] in IMAGES:
                screen.blit(IMAGES[board[row][column]],(column*SQUARE_SIZE,row*SQUARE_SIZE))

    

def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    loadImages()
    screen.fill(WHITE)
    running = True
    while running:
        clock.tick(MAX_FPS)
        for e in p.event.get():
            print(e)
            drawBoard(screen)
            if e.type == p.QUIT:
                running = False
            
        p.display.update()
        
        
if __name__ == "__main__":
    main()