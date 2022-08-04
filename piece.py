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
            self.hasMoved = False
            self.isSelected = False
            self.movesPossible: set[tuple[int, int]] = set()
        self.imageString = piece

    def updatePos(self, position):

        self.currentPos = position

    def generateMoves(self, board):
        pass

    def moved(self):
        self.hasMoved = True

    def clearMoves(self):
        self.movesPossible = set()

    def selectPiece(self):
        self.isSelected = True

    def unselectPiece(self):
        self.isSelected = False

    def checkValidCoordinate(self, pos, board):
        row = pos[0]
        column = pos[1]
        if (
            row < len(board)
            and row >= 0
            and column < len(board)
            and column >= 0
            and (board[row][column].emptyTile or self.isWhite != board[row][column].isWhite)
        ):
            return True
        return False


class Pawn(Piece):
    def __init__(self, piece, position):
        super().__init__(piece, position)

    def addIf(self, positions, board):
        for position in positions:
            row = position[0]
            column = position[1]
            if self.checkValidCoordinate((row, column), board):
                moveToMake: Piece = board[row][column]
                cond1 = self.currentPos[1] == column and moveToMake.emptyTile
                cond2 = (
                    abs(self.currentPos[0] - row) == 1
                    and abs(self.currentPos[1] - column) == 1
                    and not moveToMake.emptyTile
                    and moveToMake.isWhite != self.isWhite
                )
                if cond1 or cond2:
                    self.movesPossible.add((row, column))

    def generateMoves(self, board):
        if not self.currentPos:
            self.movesPossible = set()
            return
        if not self.currentPos:
            self.movesPossible = set()
            return
        (row, column) = self.currentPos

        if not self.hasMoved:
            if self.isWhite:
                self.addIf([(row - 1, column), (row - 2, column), (row - 1, column + 1), (row - 1, column - 1)], board)
            else:
                self.addIf([(row + 1, column), (row + 2, column), (row + 1, column + 1), (row + 1, column - 1)], board)

        else:
            if self.isWhite:
                self.addIf([(row - 1, column), (row - 1, column + 1), (row - 1, column - 1)], board)
            else:
                self.addIf([(row + 1, column), (row + 1, column + 1), (row + 1, column - 1)], board)


class Rook(Piece):
    def __init__(self, piece, position):
        super().__init__(piece, position)
        self.canCastle = True

    def addIf(self, positions, board):
        for position in positions:
            row = position[0]
            column = position[1]

            if self.checkValidCoordinate((row, column), board):
                moveToMake: Piece = board[row][column]
                self.movesPossible.add((row, column))
                if not moveToMake.emptyTile:
                    break
            else:
                break

    def generateMoves(self, board):
        if not self.currentPos:
            self.movesPossible = set()
            return
        if not self.currentPos:
            self.movesPossible = set()
            return
        (row, column) = self.currentPos
        Rook.addIf(self, [(row + i, column) for i in range(1, 8)], board)
        Rook.addIf(self, [(row - i, column) for i in range(1, 8)], board)
        Rook.addIf(self, [(row, column - i) for i in range(1, 8)], board)
        Rook.addIf(self, [(row, column + i) for i in range(1, 8)], board)


class Bishop(Piece):
    def __init__(self, piece, position):
        super().__init__(piece, position)

    def addIf(self, positions, board):
        for position in positions:
            row = position[0]
            column = position[1]

            if self.checkValidCoordinate((row, column), board):
                moveToMake: Piece = board[row][column]
                cond1 = abs(self.currentPos[1] - column) == abs(self.currentPos[0] - row)
                if cond1:
                    self.movesPossible.add((row, column))
                    if not moveToMake.emptyTile:
                        break
            else:
                break

    def generateMoves(self, board):
        if not self.currentPos:
            self.movesPossible = set()
            return

        (row, column) = self.currentPos

        Bishop.addIf(self, [(row + i, column + i) for i in range(1, 8)], board)
        Bishop.addIf(self, [(row + i, column - i) for i in range(1, 8)], board)
        Bishop.addIf(self, [(row - i, column + i) for i in range(1, 8)], board)
        Bishop.addIf(self, [(row - i, column - i) for i in range(1, 8)], board)


class King(Piece):
    def __init__(self, piece, position):
        super().__init__(piece, position)
        self.inCheck: bool = False
        self.canCastle: bool = True

    def addIf(self, positions, board):
        for position in positions:
            row = position[0]
            column = position[1]

            if self.checkValidCoordinate((row, column), board):
                self.movesPossible.add((row, column))

    def generateMoves(self, board):
        if not self.currentPos:
            self.movesPossible = set()
            return
        (row, column) = self.currentPos
        x = [
            (row - 1, column - 1),
            (row - 1, column),
            (row - 1, column + 1),
            (row, column + 1),
            (row, column - 1),
            (row + 1, column),
            (row + 1, column - 1),
            (row + 1, column + 1),
        ]
        self.addIf(x, board)


class Queen(Bishop, Rook):
    def __init__(self, piece, position):
        Piece.__init__(self, piece, position)

    def generateMoves(self, board):
        if not self.currentPos:
            self.movesPossible = set()
            return
        Rook.generateMoves(self, board)
        Bishop.generateMoves(self, board)


class Knight(Piece):
    def __init__(self, piece, position):
        super().__init__(piece, position)

    def addIf(self, positions, board):
        for position in positions:
            row = position[0]
            column = position[1]

            if self.checkValidCoordinate((row, column), board):
                self.movesPossible.add((row, column))

    def generateMoves(self, board):
        if not self.currentPos:
            self.movesPossible = set()
            return
        (row, column) = self.currentPos
        x = [
            (row - 2, column + 1),
            (row - 2, column - 1),
            (row - 1, column - 2),
            (row + 1, column - 2),
            (row - 1, column + 2),
            (row + 1, column + 2),
            (row + 2, column - 1),
            (row + 2, column + 1),
        ]
        self.addIf(x, board)
