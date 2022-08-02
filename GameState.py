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
    def __init__(self) -> None:
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
        self.moveLog = []
        self.whiteCanCastle = True
        self.blackCanCastle = True
        self.whiteScore = 0
        self.blackScore = 0
        self.blackInCheck = False
        self.whiteInCheck = False
        self.generateMoves()

    def checkPiece(self, row, column):
        return not self.board[row][column].emptyTile

    def makeMove(self, pieceSelected: piece.Piece, final):
        initial = pieceSelected.currentPos
        if final in pieceSelected.movesPossible:
            self.board[initial[0]][initial[1]] = piece.Piece("--", (initial[0], initial[1]))
            pieceSelected.updatePos((final[0], final[1]))
            self.board[final[0]][final[1]] = pieceSelected
            self.moveLog.append(Move(pieceSelected, initial, final))
            self.generateMoves()
            self.whiteMove = not self.whiteMove
            return True
        return False

    def generateMoves(self):
        for row in range(len(self.board)):
            for column in range(len(self.board)):
                self.board[row][column].clearMoves()
                self.board[row][column].generateMoves(self.board)


class Move:
    def __init__(self, piece, initial, final) -> None:
        self.initial = initial
        self.final = final
        self.piece = piece
