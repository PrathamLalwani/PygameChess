import random

import black
import piece

INIT_BOARD = [
    ["br", "bk", "bb", "bq", "bc", "bb", "bk", "br"],
    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
    ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wr", "wk", "wb", "wq", "wc", "wb", "wk", "wr"],
]


class GameState:
    def __init__(self, mode: int = 0) -> None:
        self.board: list([piece.Piece]) = [[None for i in range(len(INIT_BOARD))] for j in range(len(INIT_BOARD))]
        self.board[0][0] = piece.Rook(INIT_BOARD[0][0], (0, 0))
        self.board[0][1] = piece.Knight(INIT_BOARD[0][1], (0, 1))
        self.board[0][2] = piece.Bishop(INIT_BOARD[0][2], (0, 2))
        self.board[0][3] = piece.Queen(INIT_BOARD[0][3], (0, 3))
        self.board[0][4] = piece.King(INIT_BOARD[0][4], (0, 4))
        self.board[0][5] = piece.Bishop(INIT_BOARD[0][5], (0, 5))
        self.board[0][6] = piece.Knight(INIT_BOARD[0][6], (0, 6))
        self.board[0][7] = piece.Rook(INIT_BOARD[0][7], (0, 7))
        self.board[1] = [piece.Pawn(INIT_BOARD[1][column], (1, column)) for column in range(len(INIT_BOARD))]
        for i in range(2, 6):
            self.board[i] = [piece.Piece("--", (i, column)) for column in range(len(INIT_BOARD))]

        self.board[7][0] = piece.Rook(INIT_BOARD[7][0], (7, 0))
        self.board[7][1] = piece.Knight(INIT_BOARD[7][1], (7, 1))
        self.board[7][2] = piece.Bishop(INIT_BOARD[7][2], (7, 2))
        self.board[7][3] = piece.Queen(INIT_BOARD[7][3], (7, 3))
        self.board[7][4] = piece.King(INIT_BOARD[7][4], (7, 4))
        self.board[7][5] = piece.Bishop(INIT_BOARD[7][5], (7, 5))
        self.board[7][6] = piece.Knight(INIT_BOARD[7][6], (7, 6))
        self.board[7][7] = piece.Rook(INIT_BOARD[7][7], (7, 7))

        self.board[6] = [piece.Pawn(INIT_BOARD[6][column], (6, column)) for column in range(len(INIT_BOARD))]

        self.whiteMove = True
        self.moveLog: list[Move] = []
        self.whiteScore = 0
        self.blackScore = 0
        self.blackKing: piece.King = self.board[0][4]
        self.whiteKing: piece.King = self.board[7][4]
        self.mode = mode
        self.generateAllMoves()
        self.blackPieces: list[piece.Piece] = [self.board[i][j] for i in range(0, 2) for j in range(len(self.board))]
        self.whitePieces: list[piece.Piece] = [self.board[i][j] for i in range(6, 8) for j in range(len(self.board))]

    def checkPiece(self, row, column):
        return not self.board[row][column].emptyTile

    def makeMove(self, pieceSelected: piece.Piece, final):
        initial = pieceSelected.currentPos
        if final in pieceSelected.movesPossible:
            self.moveLog.append(Move(pieceSelected, initial, final, self.board[final[0]][final[1]]))
            self.board[initial[0]][initial[1]] = piece.Piece("--", initial)
            pieceSelected.updatePos(final)
            self.board[final[0]][final[1]].updatePos(())
            self.board[final[0]][final[1]] = pieceSelected
            self.whiteMove = not self.whiteMove

            return True

        return False

    def undoMove(self):
        if len(self.moveLog) > 0:
            move = self.moveLog.pop()
            self.board[move.initial[0]][move.initial[1]] = move.piece
            self.board[move.final[0]][move.final[1]] = move.pieceCaptured
            move.piece.updatePos(move.initial)
            move.pieceCaptured.updatePos(move.final)
            move.piece.hasMoved = False
            self.whiteMove = not self.whiteMove
            for loggedMove in self.moveLog:
                if loggedMove.piece == move.piece:
                    move.piece.moved()
            return True
        return False

    def makeAIMove(self):
        if self.mode == 1:
            moves = []
            while not moves:
                randomPiece: piece.Piece = random.choice(self.blackPieces)
                moves = randomPiece.movesPossible

        moves = list(moves)
        randomMove = random.choice(moves)
        self.makeMove(randomPiece, randomMove)

    def generateAllMoves(self):
        for row in range(len(self.board)):
            for column in range(len(self.board)):
                pieceComputing: piece.Piece = self.board[row][column]
                pieceComputing.clearMoves()
                pieceComputing.generateMoves(self.board)

    def generateMoves(self, pieces: list[piece.Piece]):
        for piece in pieces:
            piece.clearMoves()
            piece.generateMoves(self.board)

    def checkChecks(self):
        self.blackKing.inCheck = False
        for piece in self.whitePieces:
            if self.blackKing.currentPos in piece.movesPossible:
                self.blackKing.inCheck = True
        self.whiteKing.inCheck = False

        for piece in self.blackPieces:
            if self.whiteKing.currentPos in piece.movesPossible:
                self.whiteKing.inCheck = True

    def filterMoves(self):
        if self.whiteMove:
            for piece in self.whitePieces:
                if piece.currentPos == ():
                    continue
                movesPossible = set()
                movesToCheck = piece.movesPossible
                for move in movesToCheck:
                    self.whiteKing.inCheck = False
                    if self.makeMove(piece, move):
                        self.generateMoves(self.blackPieces)
                        self.checkChecks()
                        self.undoMove()
                        if not self.whiteKing.inCheck:
                            movesPossible.add(move)
                piece.movesPossible = movesPossible.copy()
        else:
            for piece in self.blackPieces:
                if piece.currentPos == ():
                    continue
                movesPossible = set()
                movesToCheck = piece.movesPossible
                for move in movesToCheck:
                    self.blackKing.inCheck = False
                    if self.makeMove(piece, move):
                        self.generateMoves(self.whitePieces)
                        self.checkChecks()
                        self.undoMove()
                        if not self.blackKing.inCheck:
                            movesPossible.add(move)
                piece.movesPossible = movesPossible.copy()


class Move:
    def __init__(self, piece, initial, final, pieceCaptured) -> None:
        self.initial = initial
        self.final = final
        self.piece = piece
        self.pieceCaptured = pieceCaptured
