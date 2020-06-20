from qango6x6 import Quango6x6
from util import test_game
def showpos(p):
	q = Quango6x6()
	q.position=p
	test_game(q)

game = Quango6x6()
game.set_state([2555035816, 8668647184], False)
showpos(game.position)