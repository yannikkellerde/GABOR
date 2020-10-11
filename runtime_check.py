from time import perf_counter
from graph_tools_games import Tic_tac_toe, Qango6x6
from graph_tool.all import *
from graph_tool_utilities import split_into_subgraphs

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
g = Graph(qango.graph)
print(f"graph copy: {perf_counter()-s}")
s = perf_counter()
subs = split_into_subgraphs(g)
print(f"split into subgraphs: {perf_counter()-s}, Result:{len(subs)}")