from qango6x6 import Quango6x6
from util import test_game
def showpos(p):
	q = Quango6x6()
	q.position=p
	test_game(q)
