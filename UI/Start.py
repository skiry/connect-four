import sys
sys.path.append('./..')
from Repo.Board import *
from Controller.Game import *
from CLI import UserInterface
from GUI import GUI

print("Graphical user interface or Command-line interface?")
while True:
	try:
		x = int(input("1 for GUI, 2 for CLI: "))
		if x not in range(1,3):
			raise ValueError("Please write 1/2")
		b = Board()
		g = Game(b)
		if x == 1:
			u = GUI(g)
		else:
			u = UserInterface(g)
	except Exception as exc:
		print(exc)
