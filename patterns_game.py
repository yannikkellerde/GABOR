from that_kind_of_game import Game
from bitops import get_least_significant_set_bit
import math
from tqdm import tqdm,trange

class Patterns_Game(Game):
    def __init__(self,win_patterns,position,onturn,squares):
        self.win_patterns = win_patterns
        self.position = position
        self.onturn = onturn
        self.squares = squares

    def sort_my_winpatterns(self):
        def get_non_uniques(winpattern):
            out = 0
            for wp in self.win_patterns:
                if wp!=winpattern:
                    out |= wp&winpattern
            return out
        def my_sort_func(winpattern):
            return ((len(get_set_bits(winpattern,self.squares))-3)*(5**5) +
                     len(get_set_bits(winpattern&self.position[0],self.squares))*(5**4) +
                     len(get_set_bits(winpattern&self.position[1],self.squares))*(5**3) +
                     len(get_set_bits(get_non_uniques(winpattern),self.squares))*(5**2) +
                     len(get_set_bits(get_non_uniques(winpattern)&self.position[0],self.squares))*5 +
                     len(get_set_bits(get_non_uniques(winpattern)&self.position[1],self.squares)))
        self.win_patterns.sort(key=my_sort_func)

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
        for start in range(self.squares):
            square = 1<<start
            score = 0
            for i,wp in enumerate(self.win_patterns):
                score += bool(square&wp)*(2**i)*3
            score += bool(square&self.position[0])*2
            score += bool(square&self.position[1])
            sammlo.append((score,start))
        sammlo.sort()
        new_pos = [0,0]
        new_winpatterns = [0 for _ in range(len(self.win_patterns))]
        for target,(_score,start) in enumerate(sammlo):
            new_pos[0] = swapin_bit(self.position[0],new_pos[0],start,target)
            new_pos[1] = swapin_bit(self.position[1],new_pos[1],start,target)
            for i in range(len(self.win_patterns)):
                new_winpatterns[i] = swapin_bit(self.win_patterns[i],new_winpatterns[i],start,target)
        for i in range(len(self.win_patterns)):
            self.win_patterns[i] = new_winpatterns[i]
        self.position = new_pos

    def __str__(self):
        mystr = ""
        for winpattern in self.win_patterns:
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
    winpatterns = []
    all_bits = set()
    for winpattern in game.winpatterns:
        and0 = winpattern&game.position[0]
        and1 = winpattern&game.position[1]
        if not ((and0 and and1) or and0==winpattern or and1==winpattern):
            winpatterns.append(winpattern)
            all_bits.update(get_set_bits(winpattern))
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
    return Patterns_Game(out_winpatterns,output_poses,game.onturn,curr_index)
