import networkx as nx
from graph_games import Tic_tac_toe
import matplotlib.pyplot as plt

def test_moving():
    game = Tic_tac_toe()
    while len(game.graph)>0:
        moves = game.get_actions()
        if moves==True:
            print("win")
            break
        #print("\n#####################\n",moves)
        #print(game.graph.nodes(data=True))
        game.draw_me(with_labels=True)
        game.make_move(moves[0])
        game.draw_me(with_labels=True)
        game.revert_moves(1)
        game.draw_me(with_labels=True)
        game.make_move(moves[0])

def test_board_representation():
    game = Tic_tac_toe()
    game.board_representation.position = list("wfffbffff")
    game.graph = game.board_representation.to_graph()
    game.hashme()
    game.draw_me(with_labels=True)

if __name__ == "__main__":
    test_board_representation()