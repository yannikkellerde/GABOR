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

    def get_burgregel_blocked(self,b_count):
        self.inv_maps()
        threadblock = set()
        if b_count==0:
            blocked_sq = []
            block_depths = set()
        if b_count==1 or b_count==2:
            blocked_sq = [7,10,14,15,20,21,25,28]
            if b_count==2:
                threadblock.add(1)
                block_depths = set([0,2])
            else:
                block_depths = set([0])
        elif b_count==3:
            blocked_sq = [7,8,9,10,13,14,15,16,19,20,21,22,25,26,27,28]
            block_depths = set([0])
        blocked_moves = set(self.node_map_rev[x] for x in blocked_sq)
        return blocked_moves,block_depths,threadblock

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

class Qango7x7(Graph_game):
    def __init__(self):
        super().__init__()
        self.board = Qango7x7_board()
        self.board.game = self
        self.graph_from_board()

class Qango7x7_board(Board_game):
    def __init__(self):
        super().__init__()
        self.squares = 49
        self.position = ["f" for _ in range(self.squares)]
        self.winsquarenums = {
            frozenset({0,1,7}),frozenset({5,6,13}),frozenset({35,42,43}),
            frozenset({41,47,48}),frozenset({2,8,14}),frozenset({4,12,20}),
            frozenset({28,36,44}),frozenset({34,40,46}),frozenset({3,9,10}),
            frozenset({26,27,33}),frozenset({29,30,37}),frozenset({11,18,19}),
            frozenset({15,21,22}),frozenset({38,39,45}),frozenset({16,17,23}),
            frozenset({25,31,32})
        }
        self.winsquarenums.update(findsquares(self.squares))
        self.winsquarenums.update(findfivers(self.squares))
        remove_useless_wsn(self.winsquarenums)

    def get_burgregel_blocked(self,b_count):
        self.inv_maps()
        threadblock = set()
        block_depths = set([0])
        if b_count==0:
            blocked_sq = []
        elif b_count==1:
            blocked_sq = [8,12,16,17,18,23,25,30,31,32,36,40]
        elif b_count==2:
            blocked_sq = [8,12,16,17,18,23,25,30,31,32,36,40,
                          9,10,11,15,19,22,26,29,33,37,38,39]
        elif b_count==3:
            blocked_sq = [8,12,16,17,18,23,25,30,31,32,36,40,
                          9,10,11,15,19,22,26,29,33,37,38,39,
                          3,21,27,45]
        blocked_moves = set(self.node_map_rev[x] for x in blocked_sq)
        return blocked_moves,block_depths,threadblock

if __name__ == "__main__":
    q = Qango7x7_board()
    print(len(q.winsquarenums))