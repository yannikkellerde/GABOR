from graph_tools_game import Graph_game
from graph_board_game import Board_game
from util import findfivers, findsquares, remove_useless_wsn
from graph_tool.all import *
import matplotlib.pyplot as plt
from collections import defaultdict

class Qango6x6(Graph_game):
    def __init__(self):
        super().__init__()
        self.board = Qango6x6_board()
        self.board.game = self
        self.graph_from_board()

class Qango6x6_board(Board_game):
    def __init__(self):
        super().__init__()
        self.squares = 36
        self.position = ["f" for _ in range(self.squares)]
        self.winsquarenums = {
            frozenset({0,1,6}),frozenset({4,5,11}),frozenset({24,30,31}),frozenset({29,34,35}),
            frozenset({2,7,12}),frozenset({3,10,17}),frozenset({18,25,32}),frozenset({23,28,33}),
            frozenset({8,13,14}),frozenset({9,15,16}),frozenset({19,20,26}),frozenset({21,22,27})
        }
        self.winsquarenums.update(findsquares(self.squares))
        self.winsquarenums.update(findfivers(self.squares))
        remove_useless_wsn(self.winsquarenums)

class Tic_tac_toe(Graph_game):
    def __init__(self):
        super().__init__()
        self.board = Tic_tac_toe_board()
        self.board.game = self
        self.graph_from_board()

class Tic_tac_toe_board(Board_game):
    def __init__(self):
        super().__init__()
        self.squares = 9
        self.position = ["f" for _ in range(self.squares)]
        self.winsquarenums = {frozenset({0,1,2}),frozenset({3,4,5}),frozenset({6,7,8}),
                              frozenset({0,3,6}),frozenset({1,4,7}),frozenset({2,5,8}),
                              frozenset({0,4,8}),frozenset({2,4,6})}