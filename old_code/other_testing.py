from qango6x6 import Qango6x6
from util import test_game
def showpos(p):
	q = Qango6x6()
	q.position=p
	test_game(q)

game = Qango6x6()
print(len(game.winpatterns))
game.set_state([2555035816, 8668647184], False)
showpos(game.position)