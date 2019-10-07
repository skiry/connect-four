import tkinter as tk
import sys
sys.path.append('./..')
from Controller.Game import *
from Class.Point import *
from Repo.Board import *
#WIN:1114234
#FORBIDDEN:124344

class GUI:
    def __init__(self,game):
        '''
        initialize the game and call the start function
        '''
        #self._board = [ [None]*7 for _ in range(6) ]
        self._game = game
        #self._root = tk.Tk()
        #self._counter = 0
        self._start()

    def _start(self):
        '''
        function which takes care of the user input, and calls other functions from different classes
        '''
        doThis = 1
        while doThis:
            try:
                user = input("Do you want to be the first? (Y/n)")
                if user.lower() != 'y' and user.lower() != 'n': 
                    raise ValueError("Please answer with Yes or No.")
                doThis = 0
                if user.lower() == 'y':
                    user = 1 # user is the first
                else:
                    user = 0 # computer is the first
            except Exception as exc:
                print(exc)

        board = [ [None]*7 for _ in range(6) ]
        counter = 0
        root = tk.Tk()

        def on_click(i,j,event,counter,user):
            if counter < 42:
                if user == 1:
                    try:
                        matrice = self._game._board._matrix
                        for ctr in range(0,6):
                            if matrice[ctr][j] == 0:
                                self._game.makeMoveUser(Point(ctr,j))
                                color = 'green'
                                #event.widget.config(bg=color)
                                board[5-ctr][j] = color
                                ctr = 10
                                break
                        if ctr != 10:
                            raise ValueError("This column is full.")
                        counter += 1
                    except Exception as exc:
                        print(exc)
                elif user == 0:
                    pcMove = self._game.makeMoveAI()
                    if pcMove[0] == False:
                        counter = 50
                        print("Congratulations !!!!!!!!!")
                    elif pcMove[0] == 7:
                        counter = 50
                        print("Maybe another time!")
                    try:
                        board[5 - pcMove[1][0]][pcMove[1][1]] = 'red'
                    except Exception:
                        pass
                    counter += 1
                print(self._game._board)
                user += 1
                user %= 2
                global gameframe
                gameframe.destroy()
                redraw(counter,user)

        def redraw(counter,user):
            global gameframe
            gameframe = tk.Frame(root)
            gameframe.pack()

            for i,row in enumerate(board):

                for j,column in enumerate(row):
                    name = str(i)+str(j)
                    L = tk.Label(gameframe,text='    ',bg= "grey" if board[i][j] == None else board[i][j])
                    L.grid(row=i,column=j,padx='3',pady='3')
                    L.bind('<Button-1>',lambda e,i=i,j=j:on_click(i,j,e,counter,user))


        redraw(counter,user)
        root.mainloop()
if __name__ == '__main__':
    b = Board()
    g = Game(b)
    u = GUI(g)




