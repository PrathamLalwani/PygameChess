from itertools import count
from re import S
from telnetlib import GA
from turtle import undo
import pygame as p
import os
from GameState import GameState
from Piece import King, Piece


# os.environ["SDL_VIDEODRIVER"] = "dummy"
# os.environ["DISPLAY"] = ":0.0"
p.font.init()

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
GAME_STATE = GameState(0)
WINNER_FONT = p.font.SysFont("Arial", 20)

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

                if isinstance(piece, King):
                    GAME_STATE.checkChecks()
                    if piece.inCheck:
                        (x, y) = piece.currentPos
                        image = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
                        image.set_alpha(100)
                        image.fill((255, 52, 62))
                        screen.blit(image, (y * SQUARE_SIZE, x * SQUARE_SIZE))

                if piece.isSelected:
                    for move in piece.movesPossible:
                        (x, y) = move.final
                        image = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
                        image.set_alpha(100)
                        image.fill((39, 251, 107))
                        screen.blit(image, (y * SQUARE_SIZE, x * SQUARE_SIZE))

                screen.blit(
                    IMAGES[piece.imageString],
                    (column * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + OFFSET),
                )
            if piece.inDanger:
                (x, y) = piece.currentPos
                image = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
                image.set_alpha(100)
                image.fill((255, 52, 62))
                screen.blit(image, (y * SQUARE_SIZE, x * SQUARE_SIZE))


def makeMoveSubRoutine():
    GAME_STATE.generateAllMoves()
    GAME_STATE.clearDanger()
    GAME_STATE.filterMoves()
    GAME_STATE.checkChecks()
    GAME_STATE.checkCheckMate()


def undoMoveSubRoutine():
    GAME_STATE.generateAllMoves()
    GAME_STATE.clearDanger()
    GAME_STATE.filterMoves()


def handleMouseClick(e, pieceSelected: Piece, landingSelected):
    position = e.pos
    column = position[0] // SQUARE_SIZE
    row = position[1] // SQUARE_SIZE
    pieceClicked: Piece = GAME_STATE.board[row][column]
    if not pieceSelected:
        # Selection logic
        if not pieceClicked.emptyTile and GAME_STATE.whiteMove == pieceClicked.isWhite: # Checks if the piece is not empty and if it is the correct color
            pieceSelected = pieceClicked # Sets the piece selected
            pieceSelected.selectPiece() # Selects the piece
    else:
        # Unselection logic
        if pieceSelected == pieceClicked:
            pieceSelected.unselectPiece()
            pieceSelected = ()
        elif not pieceClicked.emptyTile and pieceSelected.isWhite == pieceClicked.isWhite:
            pieceSelected.unselectPiece()
            pieceSelected = pieceClicked
            pieceSelected.selectPiece()

        else:
            # Move logic
            landingSelected = (row, column)
            pieceSelected.unselectPiece()
            if GAME_STATE.makeMoveFromTuple(pieceSelected, landingSelected):
                makeMoveSubRoutine()
                if GAME_STATE.mode == 1:
                    GAME_STATE.humanMove = False

            pieceSelected = None
            landingSelected = ()
    return (pieceSelected, landingSelected)


def main():

    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(WHITE)

    loadImages()
    GAME_STATE.countMoves()
    print(GAME_STATE.TOTAL_MOVES)
    running = True
    pieceSelected: Piece = None
    landingSelected = ()
    GAME_STATE.humanMove = True
    while running:
        clock.tick(MAX_FPS)
        for e in p.event.get():
            drawBoard(screen)
            if e.type == p.QUIT:
                running = False

            if GAME_STATE.pawnPromotion:
                pawnPromotionSurface = p.Surface((WIDTH // 2 - WIDTH // 4, WIDTH // 2 - WIDTH // 4),)

                screen.blit(pawnPromotionSurface, (WIDTH // 4, WIDTH // 4))
                
            if e.type == p.MOUSEBUTTONDOWN and GAME_STATE.humanMove:
                (pieceSelected, landingSelected) = handleMouseClick(e, pieceSelected, landingSelected)

            if not GAME_STATE.humanMove:
                if GAME_STATE.mode == 1 and not GAME_STATE.blackCheckMate and not GAME_STATE.whiteCheckMate:
                    GAME_STATE.makeAIMove()
                    makeMoveSubRoutine()
                    GAME_STATE.humanMove = True

            if e.type == p.KEYDOWN and e.key == p.K_DOWN:
                if GAME_STATE.undoMove():
                    undoMoveSubRoutine()
                if GAME_STATE.mode == 1:
                    if GAME_STATE.undoMove():
                        undoMoveSubRoutine()

            if GAME_STATE.whiteCheckMate or GAME_STATE.blackCheckMate:
                if GAME_STATE.whiteKing.inCheck and GAME_STATE.whiteCheckMate:
                    text = "Black Won by Checkmate"
                elif GAME_STATE.blackKing.inCheck and GAME_STATE.blackCheckMate:
                    text = "White Won by Checkmate"
                else:
                    text = "Draw by stalemate"
                p.draw.rect(
                    screen,
                    p.Color(32, 32, 32),
                    p.Rect(WIDTH // 2 - WIDTH // 4, HEIGHT // 2 - HEIGHT // 4, WIDTH // 2, HEIGHT // 2),
                )
                draw_text = WINNER_FONT.render(text, 1, p.Color("white"))
                screen.blit(
                    draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2)
                )

        p.display.update()


if __name__ == "__main__":
    main()
