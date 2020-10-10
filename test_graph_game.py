import networkx as nx
from graph_tools_games import Tic_tac_toe
import matplotlib.pyplot as plt

def test_moving():
    game = Tic_tac_toe()
    ind = 0
    while game.graph.num_vertices()>0:
        moves = game.get_actions()
        print(moves)
        if moves==True:
            print("win")
            break
        game.draw_me(ind)
        ind+=1
        game.make_move(moves[0])

def test_board_representation():
    game = Tic_tac_toe()
    game.board.position = list("wfffbffff")
    game.graph_from_board()
    game.hashme()
    game.draw_me(-1)

if __name__ == "__main__":
    #test_moving()
    test_board_representation()