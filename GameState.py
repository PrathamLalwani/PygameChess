from Piece import Piece


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
    def __init__(self) -> None:
        self.board = [
            [Piece(INIT_BOARD[row][column], (row, column)) for column in range(len(INIT_BOARD))]
            for row in range(len(INIT_BOARD))
        ]
        self.whiteMove = True
        self.moveLog = []
        self.whiteCanCastle = True
        self.blackCanCastle = True
        self.whiteScore = 0
        self.blackScore = 0
        self.blackInCheck = False
        self.whiteInCheck = False

    def checkPiece(self, row, column):
        return not self.board[row][column].emptyTile

    def makeMove(self, initial, final):
        piece = self.board[initial[0]][initial[1]]
        self.board[initial[0]][initial[1]] = Piece("--", (initial[0], initial[1]))
        piece.updatePos((final[0], final[1]))
        self.board[final[0]][final[1]] = piece
        self.moveLog.append(Move(piece, initial, final))


class Move:
    def __init__(self, piece, initial, final) -> None:
        self.initial = initial
        self.final = final
        self.piece = piece
