from re import S
import pygame as p
import os
from GameState import GameState
from piece import King, Piece

PIECES = {"br", "bk", "bb", "bq", "bc", "bp", "wr", "wk", "wb", "wq", "wc", "wp"}
MAX_FPS = 30
WIDTH, HEIGHT = 640, 640
NSQUARE = 8
SQUARE_SIZE = WIDTH // NSQUARE
WHITE = p.Color("white")
BLACK_SQUARE_IMAGE = p.image.load(os.path.join("images", "square brown dark.png"))
BLACK_SQUARE = p.transform.scale(BLACK_SQUARE_IMAGE, (SQUARE_SIZE, SQUARE_SIZE))
WHITE_SQUARE_IMAGE = p.image.load(os.path.join("images", "square brown light.png"))
OFFSET = 8
WHITE_SQUARE = p.transform.scale(WHITE_SQUARE_IMAGE, (SQUARE_SIZE, SQUARE_SIZE))
GAME_STATE = GameState(1)
IMAGES = {}


def loadImages():
    for piece in PIECES:
        IMAGES[piece] = p.transform.scale(
            p.image.load(os.path.join("images", piece + ".png")), (0.7 * SQUARE_SIZE, 0.75 * SQUARE_SIZE)
        )


def drawBoard(screen):

    rect = p.Rect(0, 0, SQUARE_SIZE, SQUARE_SIZE)
    board = GAME_STATE.board
    for row in range(NSQUARE):
        for column in range(NSQUARE):
            if (column + row) % 2 == 0:
                screen.blit(BLACK_SQUARE, (column * SQUARE_SIZE, row * SQUARE_SIZE))
            else:
                screen.blit(WHITE_SQUARE, (column * SQUARE_SIZE, row * SQUARE_SIZE))
    drawPieces(screen)


def drawPieces(screen):
    board = GAME_STATE.board
    for row in range(NSQUARE):
        for column in range(NSQUARE):
            piece: Piece = board[row][column]
            if piece.imageString in IMAGES:

                if isinstance(piece, King) and piece.inCheck:

                    (x, y) = GAME_STATE.blackKing.currentPos
                    image = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
                    image.set_alpha(100)
                    image.fill((255, 52, 62))
                    screen.blit(image, (y * SQUARE_SIZE, x * SQUARE_SIZE))

                if piece.isSelected:
                    for (x, y) in piece.movesPossible:
                        image = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
                        image.set_alpha(100)
                        image.fill((39, 251, 107))
                        screen.blit(image, (y * SQUARE_SIZE, x * SQUARE_SIZE))

                screen.blit(
                    IMAGES[piece.imageString],
                    (column * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + OFFSET),
                )


def handleMouseClick(e, pieceSelected: Piece, landingSelected):
    position = e.pos
    column = position[0] // SQUARE_SIZE
    row = position[1] // SQUARE_SIZE
    pieceClicked: Piece = GAME_STATE.board[row][column]
    if not pieceSelected:
        if not pieceClicked.emptyTile and GAME_STATE.whiteMove == pieceClicked.isWhite:
            pieceSelected = pieceClicked
            pieceSelected.selectPiece()
    else:
        if pieceSelected == pieceClicked:
            pieceSelected.unselectPiece()
            pieceSelected = ()
        elif not pieceClicked.emptyTile and pieceSelected.isWhite == pieceClicked.isWhite:
            pieceSelected.unselectPiece()
            pieceSelected = pieceClicked
            pieceSelected.selectPiece()

        else:
            landingSelected = (row, column)
            pieceSelected.unselectPiece()
            if GAME_STATE.makeMove(pieceSelected, landingSelected):
                GAME_STATE.generateAllMoves()
                GAME_STATE.checkChecks()
                if not pieceSelected.hasMoved:
                    pieceSelected.moved()
                GAME_STATE.filterMoves()
                pieceSelected = None
                landingSelected = ()
    return (pieceSelected, landingSelected)


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    loadImages()
    screen.fill(WHITE)
    running = True
    pieceSelected: Piece = None
    landingSelected = ()
    while running:
        clock.tick(MAX_FPS)
        for e in p.event.get():
            drawBoard(screen)
            if e.type == p.QUIT:
                running = False
            if e.type == p.MOUSEBUTTONDOWN:
                (pieceSelected, landingSelected) = handleMouseClick(e, pieceSelected, landingSelected)
            if e.type == p.KEYDOWN:
                if GAME_STATE.undoMove():
                    GAME_STATE.generateAllMoves()
                    GAME_STATE.filterMoves()

        p.display.update()


if __name__ == "__main__":
    main()
