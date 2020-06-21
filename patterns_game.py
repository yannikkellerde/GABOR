from that_kind_of_game import Game
from bitops import get_least_significant_set_bit
from util import getwinhash
import math
from tqdm import tqdm,trange
from copy import copy,deepcopy
from functools import reduce
import numpy as np
import pickle

class Hashable_Game(Game):
    def __init__(self,position,onturn,winhash,orig_winhash,squares):
        self.position = position
        self.onturn = onturn
        self.orig_winhash = orig_winhash
        self.winhash = deepcopy(winhash)
        self.squares = squares

    def revert_move(self,move):
        self.onturn = not self.onturn
        self.position[self.onturn] ^= move
        for wp in self.orig_winhash[move]:
            if wp not in self.winhash[move]:
                if not (wp&self.position[0] and wp&self.position[1]):
                    self.winhash[move].add(wp)

class Patterns_Game(Hashable_Game):
    def __init__(self,winpatterns,startpos,squares,zobrist_file="zobrist_hashs.pkl"):
        self.startpos = startpos
        self.squares = squares
        besetztos = (self.position[0]&self.position[1])
        self.aval_squares = set(filter(lambda x:not x&besetztos,range(self.squares)))
        self.winpatterns = winpatterns
        self.orig_winhash,self.pat_to_square = getwinhash(self.winpatterns, self.squares)
        self.winhash = deepcopy(self.orig_winhash)
        self.history = []
        self.zobrist_file = zobrist_file
        self.init_zobrist()

    def reset(self):
        super().reset()
        self.winhash = deepcopy(self.orig_winhash)
        besetztos = (self.position[0]&self.position[1])
        self.aval_squares = set(filter(lambda x:not x&besetztos,range(self.squares)))

    def get_actions(self):
        return self.aval_squares

    def revert_move(self,number=1):
        hist_index = len(self.history)-number
        self.position,self.onturn,self.aval_squares,self.winhash = self.history[hist_index]
        self.history = self.history[:hist_index]

    def make_move(self,action): 
        self.history.append([self.position.copy(),self.onturn,self.aval_squares.copy(),deepcopy(self.winhash)])
        super().make_move(action)
        self.aval_squares.discard(action)
        patterns_loosers = set()
        for wp in self.winhash[action]:
            if (wp&self.position[0] and wp&self.position[1]):
                for binsquare in self.pat_to_square[wp]:
                    if binsquare in self.aval_squares:
                        patterns_loosers.add(binsquare)
                        self.winhash[binsquare].discard(wp)
        for binsquare in patterns_loosers:
            myset = self.winhash[binsquare]
            mylen = len(myset)
            if mylen == 0:
                self.aval_squares.discard(binsquare)
            elif mylen == 1:
                wp, = myset
                if ((wp^binsquare)^(wp&self.position[0]) and (wp^binsquare)^(wp&self.position[1])):
                    self.aval_squares.discard(binsquare)
            else:
                first = True
                supersetters = set()
                for wp in myset:
                    if first:
                        supersetters.update(self.pat_to_square[wp])
                        supersetters.discard(binsquare)
                    else:
                        raus = set()
                        for suse in supersetters:
                            if not suse in self.pat_to_square[wp]:
                                raus.add(suse)
                        supersetters -= raus
                        if len(supersetters)==0:
                            break
                else:
                    self.aval_squares.discard(binsquare)

    def init_zobrist(self):
        with open(self.zobrist_file,'rb') as f:
            self.white_square_bitstrings,self.black_square_bitstrings,self.empty_square_bitstrings,self.win_pattern_bitstrings = pickle.load(f)

    def __hash__(self):
        self.shrink_myself()
        self.sort_myself()

    def shrink_myself(self):
        self.sort_poses = self.position.copy()
        self.winpatterns = reduce(lambda x,y:self.winhash[x].update(self.winhash[y]),self.winhash)
        curr_index = 0
        curr_bit = 1
        out_winpatterns = [0 for _ in self.winpatterns]
        for bit_pos in range(36):
            if len(self.winhash[bit_pos])==0:
                continue
            bit = 1<<bit_pos
            for wp in self.winhash[bit_pos]:
                index = self.winpatterns.index(wp)
                out_winpatterns[index] = out_winpatterns[index] | curr_bit
            self.sort_poses[0] = swap(self.sort_poses[0],bit_pos,curr_index,bit,curr_bit)
            self.sort_poses[1] = swap(self.sort_poses[1],bit_pos,curr_index,bit,curr_bit)
            curr_index+=1
            curr_bit = 1<<curr_index
        self.sort_poses[0] = self.sort_poses[0]&(curr_bit-1)
        self.sort_poses[1] = self.sort_poses[1]&(curr_bit-1)
        self.winpatterns = out_winpatterns
        self.shrink_squares = curr_index

    def sort_my_winpatterns(self):
        def get_non_uniques(winpattern):
            out = 0
            for wp in self.winpatterns:
                if wp!=winpattern:
                    out |= wp&winpattern
            return out
        def my_sort_func(winpattern):
            return ((len(get_set_bits(winpattern,self.shrink_squares))-3)*(5**5) +
                     len(get_set_bits(winpattern&self.sort_poses[0],self.shrink_squares))*(5**4) +
                     len(get_set_bits(winpattern&self.sort_poses[1],self.shrink_squares))*(5**3) +
                     len(get_set_bits(get_non_uniques(winpattern),self.shrink_squares))*(5**2) +
                     len(get_set_bits(get_non_uniques(winpattern)&self.sort_poses[0],self.shrink_squares))*5 +
                     len(get_set_bits(get_non_uniques(winpattern)&self.sort_poses[1],self.shrink_squares)))
        self.winpatterns.sort(key=my_sort_func)

    def sort_myself(self):
        def swapin_bit(old,new,start,target):
            start_square = 1<<start
            if start>target:
                new |= (old&start_square)>>(start-target)
            else:
                new |= (old&start_square)<<(target-start)
            return new
        self.sort_my_winpatterns()
        sammlo = []
        for start in range(self.shrink_squares):
            square = 1<<start
            score = 0
            for i,wp in enumerate(self.winpatterns):
                score += bool(square&wp)*(2**i)*3
            score += bool(square&self.sort_poses[0])*2
            score += bool(square&self.sort_poses[1])
            sammlo.append((score,start))
        sammlo.sort()
        new_pos = [0,0]
        new_winpatterns = [0 for _ in range(len(self.winpatterns))]
        for target,(_score,start) in enumerate(sammlo):
            new_pos[0] = swapin_bit(self.sort_poses[0],new_pos[0],start,target)
            new_pos[1] = swapin_bit(self.sort_poses[1],new_pos[1],start,target)
            for i in range(len(self.winpatterns)):
                new_winpatterns[i] = swapin_bit(self.winpatterns[i],new_winpatterns[i],start,target)
        for i in range(len(self.winpatterns)):
            self.winpatterns[i] = new_winpatterns[i]
        self.sort_poses = new_pos

    def __str__(self):
        mystr = ""
        for winpattern in self.winpatterns:
            mystr+=bin(winpattern)[2:].zfill(self.squares)+"\n"
        mystr+="\n"
        posstrs = [bin(x)[2:].zfill(self.squares) for x in self.position]
        mystr+="".join(["1" if posstrs[0][i]=="1" else ("2" if posstrs[1][i]=="1" else "0") for i in range(self.squares)])
        return mystr


def get_set_bits(number,max_num=36):
    return set(i for i in range(0,max_num) if (1<<i)&number)

def swap(n, p, q, bitp, bitq):
    # if bits are different at position p and q
    if (((n & bitp) >> p) ^ ((n & bitq) >> q)) == 1:
        n ^= bitp
        n ^= bitq
    return n

def convert_into_patterns_game(game:Game):
    # TODO: Filter out winpatterns that need exactly same squares to win.
    winpatterns = []
    for winpattern in game.winpatterns:
        and0 = winpattern&game.position[0]
        and1 = winpattern&game.position[1]
        if not ((and0 and and1) or and0==winpattern or and1==winpattern):
            winpatterns.append(winpattern)
    output_poses = [game.position[0],game.position[1]]
    curr_index = 0
    curr_bit = 1
    out_winpatterns = [0 for _ in winpatterns]
    my_mask = (1<<36)-1
    for bit_pos in range(36):
        bit = 1<<bit_pos
        anti_bit = bit^my_mask
        at_least_one = False
        for i in range(len(winpatterns)):
            new_wp = winpatterns[i]&anti_bit
            if new_wp != winpatterns[i]:
                at_least_one=True
                out_winpatterns[i] = out_winpatterns[i] | curr_bit
        if at_least_one:
            output_poses[0] = swap(output_poses[0],bit_pos,curr_index,bit,curr_bit)
            output_poses[1] = swap(output_poses[1],bit_pos,curr_index,bit,curr_bit)
            curr_index+=1
            curr_bit = 1<<curr_index
    output_poses[0] = output_poses[0]&(curr_bit-1)
    output_poses[1] = output_poses[1]&(curr_bit-1)
    return Patterns_Game(out_winpatterns,[output_poses,game.onturn],curr_index)
