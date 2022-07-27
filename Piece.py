PIECE_INFO = {"p": "pawn", "c": "king", "k": "knight", "q": "queen", "r": "rook", "b": "bishop"}


class Piece:
    def __init__(self, piece, position):
        if piece == "--":
            self.emptyTile = True
        else:
            self.piece = PIECE_INFO[piece[1]]
            self.isWhite = False if piece[0] == "b" else True
            self.currentPos = position
            self.emptyTile = False
            self.moveHistory = []
        self.imageString = piece

    def updatePos(self, position):
        self.moveHistory.append(self.currentPos)
        self.currentPos = position

    def getMoves(self):
        return []


class Pawn(Piece):
    def __init__(self, piece, position):
        super().__init__(piece, position)

    def getMoves(self, board):
        if len(self.moveHistory) == 0:
            (row, column) = self.currentPos
            if self.isWhite:
                return [(row - 1, column), (row - 2, column)]
            else:
                return [(row + 1, column), (row - 2, column)]


class Rook(Piece):
    def __init__(self, piece, position):
        super().__init__(piece, position)


class Bishop(Piece):
    def __init__(self, piece, position):
        super().__init__(piece, position)


class King(Piece):
    def __init__(self, piece, position):
        super().__init__(piece, position)


class Queen(Piece):
    def __init__(self, piece, position):
        super().__init__(piece, position)
