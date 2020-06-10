import math
from that_kind_of_game import Game
from util import findfivers, findsquares, getwinhash, test_game, show_all_wins,remove_useless_wsn
from bitops import bitops
from functools import reduce

class Quango6x6(Game):
    def __init__(self):
        self.winsquarenums = {
            frozenset({0,1,6}),frozenset({4,5,11}),frozenset({24,30,31}),frozenset({29,34,35}),
            frozenset({2,7,12}),frozenset({3,10,17}),frozenset({18,25,32}),frozenset({23,28,33}),
            frozenset({8,13,14}),frozenset({9,15,16}),frozenset({19,20,26}),frozenset({21,22,27})
        }
        self.squares = 36
        self.bitops = bitops()
        self.per_row = int(math.sqrt(self.squares))
        self.winsquarenums.update(findsquares(self.squares))
        self.winsquarenums.update(findfivers(self.squares))
        remove_useless_wsn(self.winsquarenums)
        self.winpatterns = list(map(lambda x:reduce(lambda y,z:y|z, list(map(lambda a:2**a, x))), self.winsquarenums))
        self.winhash = getwinhash(self.winpatterns, self.squares)
        self.reset()
        self.sortlist = [
            1<<14,1<<15,1<<20,1<<21,
            1<<7,1<<10,1<<25,1<<28,
            1<<8,1<<9,1<<13,1<<16,1<<19,1<<22,1<<26,1<<27,
            1<<2,1<<3,1<<12,1<<17,1<<18,1<<23,1<<32,1<<33,
            1<<1,1<<4,1<<6,1<<11,1<<24,1<<29,1<<31,1<<34,
            1<<0,1<<5,1<<30,1<<35
        ]
        self.fullness = (1<<36)-1
        self.sortfunc = lambda x:self.sortlist.index(x)

    def get_actions(self):
        pass #TODO

    def get_actions_simple(self):
        actions = super().get_actions()
        return sorted(actions, key=self.sortfunc)

    def get_symetries(self, pos):
        t = self.bitops.ptranspose(pos)
        r = self.bitops.preverse(pos)
        syms = [pos,
                self.bitops.pmirrorx(pos),
                self.bitops.pmirrory(pos),
                r, # rotate by 180 deg
                t, # mirror on topleft to bottomright diagonal
                self.bitops.ptranspose(r), # mirror on bottomleft to topright diagonal
                self.bitops.pmirrorx(t), # rotate by 90 deg
                self.bitops.pmirrory(t) # rotate by 270 deg
        ]
        return syms

    def extract_move(self, nextpos):
        syms = self.get_symetries(nextpos)
        for p in syms:
            xored = p[self.onturn]^self.position[self.onturn]
            if p[not self.onturn] == self.position[not self.onturn] and (xored in self.sortlist):
                return xored

    def hashpos(self):
        syms = self.get_symetries(self.position)
        ch = None
        low = math.inf
        for p in syms:
            com = (p[0]<<self.squares)|p[1]
            if com < low:
                low = com
                ch = p
        return self.bitops.encode(ch)

    def __str__(self):
        return "quango6x6"

if __name__ == "__main__":
    #test_game(Quango6x6())
    q = Quango6x6()
    print (q.check_full())
    #show_all_wins(q)