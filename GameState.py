from ast import Continue
from distutils.archive_util import make_archive
from inspect import BoundArguments
import random
import Piece
from Piece import Knight, Move, CastleMove


INIT_BOARD = [
    ["br", "bk", "bb", "bq", "bc", "bb", "bk", "br"],
    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
    ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wr", "wk", "wb", "wq", "wc", "wb", "wk", "wr"],
] # Initial board state

'''
GameState class, which holds the current state of the game, including the board, the moves, the players and the current turn.
'''
class GameState:
    TOTAL_MOVES = 0
    #
    def __init__(self, mode: int = 0, AIisWhite: bool = False) -> None:
        self.board: list([Piece.Piece]) = [[None for i in range(len(INIT_BOARD))] for j in range(len(INIT_BOARD))] # 2D array of pieces
        # Initialize board, set up black pieces
        self.board[0][0] = Piece.Rook(INIT_BOARD[0][0], (0, 0)) 
        self.board[0][1] = Piece.Knight(INIT_BOARD[0][1], (0, 1))
        self.board[0][2] = Piece.Bishop(INIT_BOARD[0][2], (0, 2))
        self.board[0][3] = Piece.Queen(INIT_BOARD[0][3], (0, 3))
        self.board[0][4] = Piece.King(INIT_BOARD[0][4], (0, 4))
        self.board[0][5] = Piece.Bishop(INIT_BOARD[0][5], (0, 5))
        self.board[0][6] = Piece.Knight(INIT_BOARD[0][6], (0, 6))
        self.board[0][7] = Piece.Rook(INIT_BOARD[0][7], (0, 7))
        self.board[1] = [Piece.Pawn(INIT_BOARD[1][column], (1, column)) for column in range(len(INIT_BOARD))]
        for i in range(2, 6):
            self.board[i] = [Piece.Piece("--", (i, column)) for column in range(len(INIT_BOARD))]
        # Set up white pieces
        self.board[7][0] = Piece.Rook(INIT_BOARD[7][0], (7, 0)) 
        self.board[7][1] = Piece.Knight(INIT_BOARD[7][1], (7, 1))
        self.board[7][2] = Piece.Bishop(INIT_BOARD[7][2], (7, 2))
        self.board[7][3] = Piece.Queen(INIT_BOARD[7][3], (7, 3))
        self.board[7][4] = Piece.King(INIT_BOARD[7][4], (7, 4))
        self.board[7][5] = Piece.Bishop(INIT_BOARD[7][5], (7, 5))
        self.board[7][6] = Piece.Knight(INIT_BOARD[7][6], (7, 6))
        self.board[7][7] = Piece.Rook(INIT_BOARD[7][7], (7, 7))

        self.board[6] = [Piece.Pawn(INIT_BOARD[6][column], (6, column)) for column in range(len(INIT_BOARD))]

        self.whiteMove = True # White moves first
        self.moveLog: list[Move] = [] # Log of moves made
        self.whiteScore = 0 # White score
        self.blackScore = 0 # Black score
        self.blackKing: Piece.King = self.board[0][4] # Black king
        self.whiteKing: Piece.King = self.board[7][4] # White king
        self.mode = mode # Mode of game
        self.AIisWhite = AIisWhite
        self.whiteCheckMate = False # Checkmate for white
        self.blackCheckMate = False # Checkmate for black
        self.humanMove = not AIisWhite 
        self.pawnPromotion: bool = False # Pawn promotion
        self.blackPieces: list[Piece.Piece] = [self.board[i][j] for i in range(0, 2) for j in range(len(self.board))] # Black pieces
        self.whitePieces: list[Piece.Piece] = [self.board[i][j] for i in range(6, 8) for j in range(len(self.board))] # White pieces
        self.generateAllMoves()
        self.filterMoves()

    def checkPiece(self, row, column):
        return not self.board[row][column].emptyTile  # Check if piece is empty

    def makeMoveFromTuple(self, pieceSelected: Piece, landingSelected):
        return self.makeMove(
            Move(
                pieceSelected,
                pieceSelected.currentPos,
                landingSelected,
                self.board[landingSelected[0]][landingSelected[1]],
            )
        ) # Make move from tuple

    
    def makeMove(self, move: Move):
        move: Move = move
        pieceSelected: Piece.Piece = move.piece
        initial = pieceSelected.currentPos
        final = move.final
        movesPossible = {temp.final for temp in pieceSelected.movesPossible}
        if final in movesPossible:
            move = next(x for x in pieceSelected.movesPossible if x.final == final)
            self.board[initial[0]][initial[1]] = Piece.Piece("--", initial)
            pieceSelected.updatePos(final)
            self.board[final[0]][final[1]].updatePos(())
            self.board[final[0]][final[1]].clearMoves()
            self.board[final[0]][final[1]] = pieceSelected
            self.whiteMove = not self.whiteMove
            if isinstance(move, CastleMove):
                secondPiece = move.secondPiece
                (secondRow, secondColumn) = move.secondInitial
                (secondFinalRow, secondFinalColumn) = move.secondFinal
                self.board[secondRow][secondColumn] = Piece.Piece("--", (secondRow, secondColumn))
                secondPiece.updatePos((secondFinalRow, secondFinalColumn))
                self.board[secondFinalRow][secondFinalColumn].updatePos(())
                self.board[secondFinalRow][secondFinalColumn].clearMoves()
                self.board[secondFinalRow][secondFinalColumn] = secondPiece
            if isinstance(pieceSelected, Piece.Pawn):
                if pieceSelected.isWhite and pieceSelected.currentPos[0] == 0:
                    self.pawnPromotion = True
                elif not pieceSelected.isWhite and pieceSelected.currentPos[0] == 7:
                    self.pawnPromotion = True

            self.moveLog.append(move)
            return True

        return False
    ''' 
    Undoes the last move made, and updates the board accordingly. 
    
    '''
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
            if isinstance(move, CastleMove):
                self.board[move.secondInitial[0]][move.secondInitial[1]] = move.secondPiece
                self.board[move.secondFinal[0]][move.secondFinal[1]] = Piece.Piece("--", move.secondFinal)
                move.secondPiece.updatePos(move.secondInitial)
                move.secondPiece.hasMoved = False

            return True
        return False
    # AI move maker, currently random
    def makeAIMove(self):
        if self.mode == 1:
            moves = []

            while not moves:
                randomPiece: Piece.Piece = random.choice(self.blackPieces)
                if not randomPiece.currentPos:
                    continue
                moves = randomPiece.movesPossible

        moves = list(moves)
        randomMove = random.choice(moves)
        self.makeMove(randomMove)

    def generateAllMoves(self):
        for row in range(len(self.board)):
            for column in range(len(self.board)):
                pieceComputing: Piece.Piece = self.board[row][column]
                pieceComputing.clearMoves()
                pieceComputing.generateMoves(self.board)

    def generateMoves(self, pieces: list[Piece.Piece]):
        for piece in pieces:
            piece.clearMoves()
            piece.generateMoves(self.board)

    def checkChecks(self):
        self.blackKing.inCheck = False
        for piece in self.whitePieces:
            movesPossible = {move.final for move in piece.movesPossible}
            if self.blackKing.currentPos in movesPossible:
                self.blackKing.inCheck = True

        self.whiteKing.inCheck = False
        for piece in self.blackPieces:
            movesPossible = {move.final for move in piece.movesPossible}
            if self.whiteKing.currentPos in movesPossible:
                self.whiteKing.inCheck = True
    # Filters moves to only allow moves that don't put the king in check
    def filterMoves(self):
        if self.whiteMove:
            for piece in self.whitePieces:
                if piece.currentPos == ():
                    continue
                movesPossible = set()
                movesToCheck: set[Move] = piece.movesPossible.copy()
                for move in movesToCheck:
                    self.whiteKing.inCheck = False
                    if self.makeMove(move):

                        self.generateMoves(self.blackPieces)
                        self.checkChecks()
                        self.undoMove()
                        if not self.whiteKing.inCheck:
                            movesPossible.add(move)
                            if not self.whiteMove:
                                self.board[move.final[0]][move.final[1]].inDanger = True
                piece.movesPossible = movesPossible.copy()
            del movesToCheck, piece, move
        else:
            for piece in self.blackPieces:
                if piece.currentPos == ():
                    continue
                movesPossible = set()
                movesToCheck = piece.movesPossible.copy()
                for move in movesToCheck:
                    self.blackKing.inCheck = False
                    if self.makeMove(move):
                        self.generateMoves(self.whitePieces)
                        self.checkChecks()
                        self.undoMove()
                        if not self.blackKing.inCheck:
                            movesPossible.add(move)
                            if self.whiteMove:
                                self.board[move.final[0]][move.final[1]].inDanger = True
                piece.movesPossible = movesPossible.copy()

            del movesToCheck, piece, move
    # Counts the number of moves possible
    def countMoves(self, depth=1):
        if depth == 0:
            return
        if self.whiteMove:
            for piece in self.whitePieces:
                self.filterMoves()
                self.TOTAL_MOVES += len(piece.movesPossible)
                for move in piece.movesPossible:
                    self.makeMove(move)
                    self.countMoves(depth)
                    self.undoMove()
        else:
            for piece in self.blackPieces:
                self.TOTAL_MOVES += len(piece.movesPossible)
                for move in piece.movesPossible:
                    self.makeMove(move)
                    self.countMoves(depth - 1)
                    self.undoMove()
    # Checks if the game is over
    def checkCheckMate(self):
        if self.whiteMove:
            self.whiteCheckMate = all([len(piece.movesPossible) == 0 for piece in self.whitePieces])
        else:
            self.blackCheckMate = all([len(piece.movesPossible) == 0 for piece in self.blackPieces])
    # Removes the check from the king
    def clearDanger(self):
        for row in self.board:
            for piece in row:
                piece.inDanger = False
    # Checks if the castling move is valid
    def canCastle(self, king: Piece.King, rook: Piece.Rook):
        if not king.hasMoved and king.inDanger:
            (row, column) = king.currentPos
            (row2, column2) = rook.currentPos
