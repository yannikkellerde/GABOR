from time import perf_counter
from graph_games import Tic_tac_toe, Qango6x6

s = perf_counter()
qango = Qango6x6()
print(f"Initialization {perf_counter()-s}")
s = perf_counter()
qango.hashme()
print(f"Hashing {perf_counter()-s}")
s = perf_counter()
moves = qango.get_actions()
print(f"get_actions: {perf_counter()-s}")
s = perf_counter()
qango.make_move(moves[0])
print(f"make_move: {perf_counter()-s}")
s = perf_counter()
g = qango.graph.copy()
print(f"graph copy: {perf_counter()-s}")