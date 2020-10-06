import networkx as nx
from graph_games import Tic_tac_toe
import matplotlib.pyplot as plt

game = Tic_tac_toe()
moves = game.get_actions()
print(moves)
print(game.graph.nodes(data=True))
game.draw_me(with_labels=True)