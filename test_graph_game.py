import networkx as nx
from graph_tools_games import Tic_tac_toe,Qango6x6
from solve_graph_tools import PN_search
import matplotlib.pyplot as plt
import time

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
    game.board.position = list("fbf"
                               "wbb"
                               "wfw")
    game.board.onturn = "w"
    game.graph_from_board()
    game.hashme()
    moves = game.get_actions()
    print(moves)
    game.make_move(moves[1])
    game.draw_me(-1)

def test_forced_move_search():
    game = Qango6x6()
    game.board.position = list( "ffffff"
                                "fbwwbf"
                                "ffffff"
                                "ffwfff"
                                "fffbff"
                                "ffffff")
    game.board.onturn = "b"
    game.graph_from_board()
    game.hashme()
    game.draw_me(-1)
    s = time.perf_counter()
    print(game.forced_move_search())
    print(time.perf_counter()-s)

if __name__ == "__main__":
    #test_moving()
    #test_board_representation()
    test_forced_move_search()