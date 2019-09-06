from qango6x6 import Quango6x6
from util import test_game
def showpos(p):
	q = Quango6x6()
	q.position=p
	test_game(q)

game = Quango6x6()
game.set_state([(1<<8)|(1<<13)|(1<<21),(1<<2)|(1<<14)|(1<<19)], True)
showpos(game.position)