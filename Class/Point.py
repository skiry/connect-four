class Point:
    '''
    Point represented by 2 coordinates
    '''
    def __init__(self,x,y):
        '''
        Constructor
        '''
        self._x = x
        self._y = y

    def getX(self):
        '''
        X coordinate getter
        '''
        return self._x

    def getY(self):
        '''
        Y coordinate getter
        '''
        return self._y
