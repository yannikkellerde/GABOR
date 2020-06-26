from patterns_game import Patterns_Game
from qango6x6 import Qango6x6_base
from util import findfivers, findsquares, remove_useless_wsn
from functools import reduce

class Tic_tac_toe(Patterns_Game):
    def __init__(self,startpos=[[0,0],True],zobrist_file="zobrist.pkl"):
        squares = 9
        winpatterns = [
            (1<<0)|(1<<1)|(1<<2),
            (1<<3)|(1<<4)|(1<<5),
            (1<<6)|(1<<7)|(1<<8),
            (1<<0)|(1<<3)|(1<<6),
            (1<<1)|(1<<4)|(1<<7),
            (1<<2)|(1<<5)|(1<<8),
            (1<<0)|(1<<4)|(1<<8),
            (1<<2)|(1<<4)|(1<<6)
        ]
        super().__init__(winpatterns,startpos,squares,zobrist_file)

    def basic_hash(self):
        return hash(self)

class Qango6x6(Patterns_Game,Qango6x6_base):
    def __init__(self,startpos=[[0,0],True],zobrist_file="zobrist.pkl"):
        squares = 36
        self.winsquarenums = {
            frozenset({0,1,6}),frozenset({4,5,11}),frozenset({24,30,31}),frozenset({29,34,35}),
            frozenset({2,7,12}),frozenset({3,10,17}),frozenset({18,25,32}),frozenset({23,28,33}),
            frozenset({8,13,14}),frozenset({9,15,16}),frozenset({19,20,26}),frozenset({21,22,27})
        }
        self.winsquarenums.update(findsquares(squares))
        self.winsquarenums.update(findfivers(squares))
        remove_useless_wsn(self.winsquarenums)
        winpatterns = list(map(lambda x:reduce(lambda y,z:y|z, list(map(lambda a:2**a, x))), self.winsquarenums))
        super().__init__(winpatterns,startpos,squares,zobrist_file)

    def basic_hash(self):
        return super().hashpos()