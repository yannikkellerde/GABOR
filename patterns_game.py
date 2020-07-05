from that_kind_of_game import Game
from bitops import get_least_significant_set_bit
from util import getwinhash
import math
from tqdm import tqdm,trange
from copy import copy,deepcopy
from functools import reduce
import time
import numpy as np
import pickle

class Patterns_Game(Game):
    def __init__(self,winpatterns,startpos,squares,zobrist_file):
        self.startpos = startpos
        self.squares = squares
        self.fullness = (1<<self.squares)-1
        super().reset()
        self.winpatterns = winpatterns
        self.orig_winhash,self.pat_to_square = getwinhash(self.winpatterns, self.squares)
        self.reset()
        self.clean_winpatterns_and_aval(self.winpatterns)
        self.history = []
        self.zobrist_file = zobrist_file
        self.init_zobrist()

    def set_state(self,position,onturn):
        super().set_state(position,onturn)
        self.winhash = deepcopy(self.orig_winhash)
        besetztos = (self.position[0]|self.position[1])
        self.aval_squares = set(filter(lambda x:not x&besetztos,(1<<y for y in range(self.squares))))
        self.clean_winpatterns_and_aval(self.winpatterns)

    def reset(self):
        super().reset()
        self.winhash = deepcopy(self.orig_winhash)
        besetztos = (self.position[0]&self.position[1])
        self.aval_squares = set(filter(lambda x:not x&besetztos,(1<<y for y in range(self.squares))))

    def get_actions(self):
        return sorted(self.aval_squares,key=lambda x:-len(self.winhash[x]))

    def revert_move(self,number=1):
        hist_index = len(self.history)-number
        self.position,self.onturn,self.aval_squares,self.winhash = self.history[hist_index]
        self.history = self.history[:hist_index]

    def clean_winpatterns_and_aval(self,care_patterns):
        patterns_loosers = set()
        discardcombos = set()
        for wp in care_patterns:
            if (wp&self.position[0] and wp&self.position[1]):
                for binsquare in self.pat_to_square[wp]:
                    patterns_loosers.add(binsquare)
                    discardcombos.add((binsquare,wp))
        for binsquare,wp in discardcombos:
            self.winhash[binsquare].discard(wp)
        self._clean_aval(patterns_loosers)

    def make_move(self,action): 
        self.history.append([self.position.copy(),self.onturn,self.aval_squares.copy(),deepcopy(self.winhash)])
        super().make_move(action)
        self.aval_squares.discard(action)
        self.clean_winpatterns_and_aval(self.winhash[action])
    def _clean_aval(self,patterns_loosers):
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
            self.bitstrings = pickle.load(f)

    def __hash__(self):
        def bit_hash_func(bit_pos):
            score = 0
            bit = 1<<bit_pos
            if bit&self.position[0]:
                score ^= self.bitstrings[0]
            elif bit&self.position[1]:
                score ^= self.bitstrings[1]
            combo_winpats = []
            for wp in self.winpatterns:
                if bit&wp:
                    score ^= winscores[wp]
                    combo_winpats.append(wp)
            if len(combo_winpats)==0:
                return 0
            #elif len(combo_winpats)==1:
            #    if (((self.position[0]&combo_winpats[0])|bit)^combo_winpats[0]) and (((self.position[1]&combo_winpats[0])|bit)^combo_winpats[0]):
            #        return 0
            return score
        self.winpatterns = set()
        for _key,value in self.winhash.items():
            self.winpatterns.update(value)
        self.winpatterns = list(self.winpatterns)
        winscores = self.score_winpatterns(self.winpatterns)
        return int(reduce(lambda x,y:x^y, map(bit_hash_func,range(self.squares))))

    def score_winpatterns(self,winpatterns):
        def get_non_uniques(winpattern):
            out = 0
            for wp in self.winpatterns:
                if wp!=winpattern and wp&winpattern:
                    out += 1 + set_bits_count[wp][0]+5*set_bits_count[wp][1]
            return out
        def my_score_func(winpattern):
            return   (self.bitstrings[(len(get_set_bits(winpattern,self.squares))-3)+2] ^
                     self.bitstrings[set_bits_count[winpattern][0]+20] ^
                     self.bitstrings[set_bits_count[winpattern][1]+40] ^
                     self.bitstrings[(get_non_uniques(winpattern)+60)%len(self.bitstrings)])
        set_bits_count = {x:(len(get_set_bits(x&self.position[0],self.squares)),len(get_set_bits(x&self.position[1],self.squares))) for x in winpatterns}
        return {x:my_score_func(x) for x in winpatterns}

    def shrink_myself(self):
        self.sort_poses = self.position.copy()
        self.winpatterns = set()
        for _key,value in self.winhash.items():
            self.winpatterns.update(value)
        self.winpatterns = list(self.winpatterns)
        curr_index = 0
        curr_bit = 1
        out_winpatterns = [0 for _ in self.winpatterns]
        for bit_pos in range(self.squares):
            bit = 1<<bit_pos
            if len(self.winhash[bit])==0:
                continue
            for wp in self.winhash[bit]:
                index = self.winpatterns.index(wp)
                out_winpatterns[index] = out_winpatterns[index] | curr_bit
            self.sort_poses[0] = swap(self.sort_poses[0],bit_pos,curr_index,bit,curr_bit)
            self.sort_poses[1] = swap(self.sort_poses[1],bit_pos,curr_index,bit,curr_bit)
            curr_index+=1
            curr_bit = 1<<curr_index
        self.sort_poses[0] = self.sort_poses[0]&(curr_bit-1)
        self.sort_poses[1] = self.sort_poses[1]&(curr_bit-1)
        self.shrink_winpatterns = out_winpatterns
        self.shrink_squares = curr_index

    def sort_myself(self):
        def swapin_bit(old,new,start,target):
            start_square = 1<<start
            if start>target:
                new |= (old&start_square)>>(start-target)
            else:
                new |= (old&start_square)<<(target-start)
            return new
        def bit_sort_func(bit_pos):
            score = 0
            bit = 1<<bit_pos
            if bit&self.sort_poses[0]:
                score += 1<<46
            elif bit&self.sort_poses[1]:
                score += 1<<47
            wslist = []
            for wp in self.shrink_winpatterns:
                if bit&wp:
                    score += (1<<40)
                    wslist.append(winscores[wp])
            score += reduce(lambda x,y:x^y,wslist)
            return score
        winscores = self.score_winpatterns(self.shrink_winpatterns)
        sort_bits = sorted(range(self.shrink_squares),key=bit_sort_func)
        new_pos = [0,0]
        new_winpatterns = [0 for _ in range(len(self.shrink_winpatterns))]
        for target,start in enumerate(sort_bits):
            new_pos[0] = swapin_bit(self.sort_poses[0],new_pos[0],start,target)
            new_pos[1] = swapin_bit(self.sort_poses[1],new_pos[1],start,target)
            for i in range(len(self.shrink_winpatterns)):
                new_winpatterns[i] = swapin_bit(self.shrink_winpatterns[i],new_winpatterns[i],start,target)
        self.shrink_winpatterns = sorted(new_winpatterns)
        self.sort_poses = new_pos

    def __str__(self):
        mystr = ""
        for winpattern in self.shrink_winpatterns:
            mystr+=bin(winpattern)[2:].zfill(self.shrink_squares)+"\n"
        mystr+="\n"
        posstrs = [bin(x)[2:].zfill(self.shrink_squares) for x in self.sort_poses]
        mystr+="".join(["1" if posstrs[0][i]=="1" else ("2" if posstrs[1][i]=="1" else "0") for i in range(self.shrink_squares)])
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
