from qango6x6 import Quango6x6
from util import test_game
def showpos(p):
	q = Quango6x6()
	q.position=p
	test_game(q)

game = Quango6x6()
print(len(game.winsquarenums))
#game.set_state([(1<<8),(1<<2)|(1<<20)], True)
#showpos(game.position)