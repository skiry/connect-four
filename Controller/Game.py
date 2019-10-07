import sys
sys.path.append('./..')
from Repo.Board import *
from Class.Point import *
from random import randint

class Game:
    def __init__(self,board):
        self._board = board

    def makeMoveUser(self,point):
        self._board.addPoint(point, 1)

    def makeMoveAI(self):
        moves = self._board.avMoves()
        '''
        #SEE THE AVAILABLE MOVES
        for j in range(1,7):
            if j in moves:
                print("INDEX : ", j)
                for x in moves[j]:
                    print(x.getX(),x.getY())
        '''
        done = 0
        if 7 in moves:
            return [False] # user won. bye
        for x in range(1,7):
            if x in moves and done == 0:
                for y in moves[x]:
                    belowPoint = Point(y.getX() - 1, y.getY())
                    if (y.getX() == 0 or self._board.okPoint(belowPoint) == True) and done == 0:
                        self._board.addPoint(y)
                        res = [y.getX(),y.getY()]
                        done = x
        if done == 0:
            if 8 in moves:
                x = randint(0,len(moves[8]) - 1)
                self._board.addPoint(moves[8][x])
                res = [moves[8][x].getX(), moves[8][x].getY()]
        if done == 1 or 100 in moves:
            return [7,res] # AI won. bye too
        return [True,res]

    def getBoard(self):
        return self._board
