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
    def __str__(self):
        return "qango6x6"

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
        elif b_count==4:
            self.position = list("ffffff"
                                 "ffffff"
                                 "ffffff"
                                 "ffffff"
                                 "fffwff"
                                 "fffbff")
            self.onturn = "b"
            self.game.graph_from_board()
            blocked_sq = [22]
            block_depths = set([0])
        self.inv_maps()
        blocked_moves = set(self.node_map_rev[x] for x in blocked_sq)
        return blocked_moves,block_depths,threadblock

class Tic_tac_toe(Graph_game):
    def __init__(self):
        super().__init__()
        self.board = Tic_tac_toe_board()
        self.board.game = self
        self.graph_from_board()
    def __str__(self):
        return "tic_tac_toe"

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
    def __str__(self):
        return "qango7x7"

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
        threatblock = set()
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
        return blocked_moves,block_depths,threatblock

class Qango7x7_plus(Graph_game):
    def __init__(self):
        super().__init__()
        self.board = Qango7x7_plus_board()
        self.board.game = self
        self.graph_from_board()
    def __str__(self):
        return "qango7x7_plus"

class Qango7x7_plus_board(Board_game):
    def __init__(self):
        super().__init__()
        self.squares = 37
        self.position = ["f" for _ in range(self.squares)]
        self.winsquarenums = {
            frozenset({2,8,14}),frozenset({4,12,20}),
            frozenset({28,36,44}),frozenset({34,40,46}),frozenset({3,9,10}),
            frozenset({26,27,33}),frozenset({29,30,37}),frozenset({11,18,19}),
            frozenset({15,21,22}),frozenset({38,39,45}),frozenset({16,17,23}),
            frozenset({25,31,32})
        }
        self.winsquarenums.update(findsquares(49))
        self.winsquarenums.update(findfivers(49))
        remove_useless_wsn(self.winsquarenums)
        self.change_wsn()

    def change_wsn(self):
        removals = [0,1,5,6,7,13,35,42,43,41,47,48]
        new_wsn = set()
        for wsn in self.winsquarenums:
            new = set()
            for ws in wsn:
                if ws in removals:
                    break
                for i,r in enumerate(removals):
                    if r>ws:
                        break
                unders = i
                new.add(ws-unders)
            else:
                new_wsn.add(frozenset(new))
        self.winsquarenums = new_wsn

    def draw_me(self,pos=None):
        row_starts = [2,1,0,0,0,1,2]
        row_ends = [5,6,7,7,7,6,5]
        out = "#"*(7+2)+"\n"
        count = 0
        pos = self.position if pos is None else pos
        for rs,re in zip(row_starts,row_ends):
            out+=" "*rs+"#"
            for _ in range(rs,re):
                out+=pos[count]
                count+=1
            out+="#"+" "*re+"\n"
        out += "#"*(7+2)
        print(out)
        return out

    def get_burgregel_blocked(self,b_count):
        self.inv_maps()
        threadblock = set()
        block_depths = set([0])
        if b_count==0:
            blocked_sq = []
        elif b_count==1:
            blocked_sq = [4,5,6,9,10,11,12,13,16,17,18,19,20,23,24,25,26,27,30,31,32]
        elif b_count==2:
            allowed = [6,13,23,30]
            blocked_sq = list(filter(lambda x:x not in allowed,range(self.squares)))
        blocked_moves = set(self.node_map_rev[x] for x in blocked_sq)
        return blocked_moves,block_depths,threadblock


if __name__ == "__main__":
    q = Qango7x7_board()
    print(len(q.winsquarenums))