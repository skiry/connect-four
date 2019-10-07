import sys
sys.path.append('./..')
from Class.Point import *
class Board:
    def __init__(self): 
        '''
        dict[0] : ai's taken positions
        dict[1] : user's taken positions
        '''
        self._dict = {}
        self._matrix = [[0,0,0,0,0,0,0,0,0,0,0,0,0]]
        for i in range(10):
            self._matrix.append([0,0,0,0,0,0,0,0,0,0,0,0])

    def addPoint(self, point, user = 0):
        '''
        add point to the list of user's points
        '''
        if user not in self._dict:
            self._dict[user] = [(point)]
        else:
            self._dict[user].append(point)
        self._matrix[point.getX()][point.getY()] = user + 1

    @staticmethod
    def changePlayer(user = 0):
        '''
        swipes the player
        0 -> 1
        1 -> 0
        '''
        user += 1
        user %= 2
        return user

    def avMoves(self):
        '''
        available moves for AI
        dict[1] : positions from where i can win immediately
        dict[2] : positions that block immediate win for the opponent(3in a row/2+space+1/vice-versa)
        dict[3] : if i put here, he will win in the next move-!FORBIDDEN!
        dict[4] : i have 2 in a row, put the 3rd
        dict[5] : next to one of AI's positions
        dict[6] : next to user
        dict[7] : isGameWon: 1=User Win
        dict[8] : random position
        '''
        positions = {}
        # 7 positions next to the actual point.
        # for the 3rd point in a row, 2*posX+2*posY
        posX = [0,0,1,1,-1,-1,1]
        posY = [-1,1,0,1,1,-1,-1]
        for j in range(0,7):
            if self._matrix[0][j] == 0:
                if 8 not in positions:
                    positions[8] = [(Point(0,j))]
                else:
                    positions[8].append(Point(0,j))

        if 0 not in self._dict and 1 not in self._dict:
            return positions
        if 0 in self._dict:
            for i in self._dict[0]:
                '''
                check my positions
                '''
                for x in range(0,7):
                    if self._matrix[i.getX() + posX[x]][i.getY() + posY[x]] == 1:
                        '''
                        first neighbour
                        '''
                        #print(i.getX(),i.getY(),i.getX() + 2*posX[x],i.getY() + 2*posY[x],i.getX() + 3*posX[x],i.getY() + 3*posY[x])
                        if self._matrix[i.getX() + 3*posX[x]][i.getY() + 3*posY[x]] == 1:
                            if self._matrix[i.getX() + 2*posX[x]][i.getY() + 2*posY[x]] == 0:
                                if self._matrix[i.getX() + 2*posX[x] - 1][i.getY() + 2*posY[x]]:
                                    #if i have 00 0, so AI wins
                                    punct = Point(i.getX() + 2*posX[x], i.getY() + 2*posY[x])
                                    #punct = the 3rd point between 2 points on a side and 1 point on another
                                    if self.inRange(punct):
                                        if 1 not in positions:
                                            positions[1] = [(punct)]
                                        else:
                                            positions[1].append(punct)
                        if self._matrix[i.getX() + 2*posX[x]][i.getY() + 2*posY[x]] == 1:
                            '''
                            second neighbour
                            '''
                            if self._matrix[i.getX() + 3*posX[x]][i.getY() + 3*posY[x]] == 1:
                                positions[100] = 1
                                #if i have 4 in a row
                            punct = Point(i.getX() + 3*posX[x], i.getY() + 3*posY[x])
                            #punct = the 4th point that can make AI win
                            belowPoint = Point(i.getX() + 3*posX[x] - 1, i.getY() + 3*posY[x])
                            #belowPoint = the point under punct
                            if self.inRange(punct) and (self.okPoint(belowPoint) == True or (i.getX() + 3*posX[x]) == 0):
                                if 1 not in positions:
                                    positions[1] = [(punct)]
                                else:
                                    positions[1].append(punct)
                            punct = Point(i.getX() - posX[x], i.getY() - posY[x])
                            belowPoint = Point(i.getX() - posX[x] - 1, i.getY() - posY[x])
                            if self.inRange(punct) and (self.okPoint(belowPoint) == True or (i.getX() - posX[x] - 1) == 0):
                                if 1 not in positions:
                                    positions[1] = [(punct)]
                                else:
                                    positions[1].append(punct)
                        else:
                            punct = Point(i.getX() + 2*posX[x], i.getY() + 2*posY[x])
                            #punct = the 3rd point in a row
                            if self.inRange(punct):
                                if 4 not in positions:
                                    positions[4] = [(punct)]
                                else:
                                    positions[4].append(punct)
                            punct = Point(i.getX() - posX[x], i.getY() - posY[x])
                            if self.inRange(punct):
                                if 4 not in positions:
                                    positions[4] = [(punct)]
                                else:
                                    positions[4].append(punct)
                    else:
                        punct = Point(i.getX() + posX[x], i.getY() + posY[x])
                        #punct = a neighbour of the actual point
                        if self.inRange(punct):
                            if 5 not in positions:
                                positions[5] = [(punct)]
                            else:
                                positions[5].append(punct)
                        punct = Point(i.getX() - posX[x], i.getY() - posY[x])
                        if self.inRange(punct):
                            if 5 not in positions:
                                positions[5] = [(punct)]
                            else:
                                positions[5].append(punct)

        for i in self._dict[1]:
            '''
            check opponent's positions
            '''
            for x in range(0,7):
                if self._matrix[i.getX() + posX[x]][i.getY() + posY[x]] == 2:
                    '''
                    first neighbour
                    '''
                    if self._matrix[i.getX() + 2*posX[x]][i.getY() + 2*posY[x]] == 2:
                        '''
                        second neighbour
                        he has 3 in a row-> we try to block his move
                        hopefully, it has only one side available, otherwise, we lose the match
                        '''
                        if self._matrix[i.getX() + 3*posX[x]][i.getY() + 3*posY[x]] == 2:
                            positions[7] = 1
                        punct = Point(i.getX() + 3*posX[x], i.getY() + 3*posY[x])
                        #punct = the 4th point that could block his win
                        if self.inRange(punct):
                            if 2 not in positions:
                                positions[2] = [(punct)]
                            else:
                                positions[2].append(punct)
                        punct = Point(i.getX() - posX[x], i.getY() - posY[x])
                        #punct = the 4th point, but placed in the opposite side
                        if self.inRange(punct):
                            if 2 not in positions:
                                positions[2] = [(punct)]
                            else:
                                positions[2].append(punct)
                    elif self._matrix[i.getX() + 3*posX[x]][i.getY() + 3*posY[x]] == 2:
                        punct = Point(i.getX() + 2*posX[x], i.getY() + 2*posY[x])
                        # OO O, punct represents the missing point
                        if self.inRange(punct):
                            if 2 not in positions:
                                positions[2] = [(punct)]
                            else:
                                positions[2].append(punct)
                else:
                    punct = Point(i.getX() + posX[x], i.getY() + posY[x])
                    #punct = point next to user
                    if self.inRange(punct):
                        if 6 not in positions:
                            positions[6] = [(punct)]
                        else:
                            positions[6].append(punct)
                    punct = Point(i.getX() - posX[x], i.getY() - posY[x])
                    #punct = point next to user
                    if self.inRange(punct):
                        if 6 not in positions:
                            positions[6] = [(punct)]
                        else:
                            positions[6].append(punct)

        return positions

    def inRange(self,point):
        '''
        check if point is in range : x-[0,5],y-[0,6]
        '''
        if point.getX() not in range(0,6) or point.getY() not in range(0,7):
            return False
        if self._matrix[point.getX()][point.getY()]:
            return False
        return True

    def okPoint(self,point):
        '''
        check if point is in range, but taken
        '''
        x = point.getX()
        y = point.getY()
        if x in range(0,6) and y in range(0,7) and self._matrix[x][y]:
            return True         # it is in range, and taken
        return 9

    def __str__(self):
        '''
        print the board
        '''
        result = ""
        line = "---------------"

        result += line
        result += '\n'
        for i in range(0,6):
            for j in range(0,7):
                result += "|"
                if self._matrix[5-i][j] == 1:
                    result += '\x1b[1;33;44m'+"O"+'\x1b[0m'
                elif self._matrix[5-i][j] == 2:
                    result += '\x1b[6;30;47m'+"O"+'\x1b[0m'
                else:
                    result += " "
            result += "|"
            result += '\n' + line + '\n'
        return result
'''
puncte = [Point(0,5), Point(0,6), Point(6,5), Point(6,6), Point(7,6), Point(7,5), Point(1,4)]
Board = Board()
Board.addPoint(Point(1,3),0)
Board.addPoint(Point(1,4),1)
Board.addPoint(Point(2,4),0)
Board.addPoint(Point(0,1),1)
Board.addPoint(Point(5,6))
Board.addPoint(Point(3,5))
Board.addPoint(Point(0,5),1)
Board.addPoint(Point(3,2),1)
#Board.addPoint(Point(2,3),1)
for i in puncte:
    print(Board.inRange(i))
moves = Board.avMoves()
for i in moves:
    print(i)
    for x in moves[i]:
        print(x.getX(),x.getY())
print(Board)
'''
