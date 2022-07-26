
from matplotlib.pyplot import pie
import numpy as np
from pyparsing import col


PIECES = {'br','bk','bb','bq','bc','bp','wr','wk','wb','wq','wc','wp'}

class GameState():
    
    def __init__(self) -> None:
        self.board = [
            ['br','bk','bb','bq','bc','bb','bk','br'],
            ['bp','bp','bp','bp','bp','bp','bp','bp'],
            ['--','--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--','--'],
            ['wp','wp','wp','wp','wp','wp','wp','wp'],
            ['wr','wk','wb','wq','wc','wb','wk','wr']        
        ]
        self.whiteMove = True
        self.moveLog = []
        
    def checkPiece(self,row,column):
        if self.board[row][column] in PIECES:
            return True
        else:
            return False
        
    def makeMove(self, initial, final):
        piece = self.board[initial[0]][initial[1]]
        self.board[initial[0]][initial[1]]  = '--'
        self.board[final[0]][final[1]] = piece
        self.moveLog.append((piece,initial,final))
        
        