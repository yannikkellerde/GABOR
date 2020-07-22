import math
import util
import gc
import sys
from patterns_game import Patterns_Game
from util import draw_board
from data_magic import save_sets

# Node storage for memory efficency in lists
PN = 0 # int
DN = 1 # int
HASH = 2 # int
PARENTS = 3 # List of Nodes(which are lists)
CHILDREN = 4 # List of tuples containing move made and Node (which is a lists)

class PN_search():
    def __init__(self, game:Patterns_Game, endgame_depth:int, drawproves=True,prooffile="provenset.txt",disprooffile="disprovenset.txt",
                 endgame_prooffile="endproven.txt",endgame_disprooffile="enddisproven.txt"):
        self.game = game
        self.ttable = {}
        self.ttable_endgame = {}
        self.provenset = set()
        self.disprovenset = set()
        self.endgame_provenset = set()
        self.endgame_disprovenset = set()
        self.endgame_depth = endgame_depth
        self.node_count = 0
        self.proofadds = [0,0]
        self.endgame_proofadds = [0,0]
        self.drawproves = drawproves
        self.prooffile = prooffile
        self.disprooffile = disprooffile
        self.endgame_prooffile = endgame_prooffile
        self.endgame_disprooffile = endgame_disprooffile
        self.loadsets()

    def loadsets(self):
        try:
            with open(self.prooffile,"r") as file:
                self.provenset = set([int(x) for x in file.read().split(",")[:-1]])
        except Exception as e:
            print(e)
        try:
            with open(self.disprooffile,"r") as file:
                self.disprovenset = set([int(x) for x in file.read().split(",")[:-1]])
        except Exception as e:
            print(e)
        try:
            with open(self.endgame_prooffile,"r") as file:
                self.endgame_provenset = set([int(x) for x in file.read().split(",")[:-1]])
        except Exception as e:
            print(e)
        try:
            with open(self.endgame_disprooffile,"r") as file:
                self.endgame_disprovenset = set([int(x) for x in file.read().split(",")[:-1]])
        except Exception as e:
            print(e)
    
    def set_pn_dn(self, n, depth):
        if n[PN] == 0 or n[DN] == 0:
            return
        if (depth+self.game.startpos[1])%2:
            n[PN] = math.inf; n[DN] = 0
            for _,c in n[CHILDREN]:
                n[DN] += c[DN]
                n[PN] = min(n[PN], c[PN])
        else:
            n[DN] = math.inf; n[PN] = 0
            for _,c in n[CHILDREN]:
                n[PN] += c[PN]
                n[DN] = min(n[DN], c[DN])

    def delete_node(self, n, ps, ch, depth):
        for p in ps:
            for i in range(len(p[CHILDREN])):
                if p[CHILDREN][i][1]==n:
                    del p[CHILDREN][i]
                    break
        for _,c in ch:
            if len(c)>PARENTS:
                c[PARENTS].remove(n)
                if len(c[PARENTS])==0:
                    self.delete_node(c, [], c[CHILDREN].copy(),depth+1)
        if depth<self.endgame_depth:
            del self.ttable[n[HASH]]
        else:
            del self.ttable_endgame[n[HASH]]
        if n[PN] == 0:
            if depth<self.endgame_depth:
                self.provenset.add(n[HASH])
                self.proofadds[0] += 1
            else:
                self.endgame_provenset.add(n[HASH])
                self.endgame_proofadds[0] += 1
        elif n[DN] == 0:
            if depth<self.endgame_depth:
                self.disprovenset.add(n[HASH])
                self.proofadds[1] += 1
            else:
                self.endgame_disprovenset.add(n[HASH])
                self.endgame_proofadds[1] += 1
        del n[CHILDREN]
        del n[PARENTS]
        # Do not use n aferwards
    
    def update_anchestors(self, n, depth):
        old_pn = n[PN]
        old_dn = n[DN]
        self.set_pn_dn(n,depth)
        if n[PN] == old_pn and n[DN] == old_dn and n[PN]!=0 and n[DN]!=0:
            return depth
        mindepth = depth
        for p in n[PARENTS].copy():
            if len(p)>3:
                adepth = self.update_anchestors(p,depth-1)
                if adepth<mindepth:
                    mindepth = adepth
        if (n[PN] == 0 or n[DN] == 0) and len(n)>PARENTS:
            self.delete_node(n, n[PARENTS], n[CHILDREN],depth)
        return max(mindepth,0)

    def select_most_proving(self, n, depth):
        path = []
        while n[CHILDREN]:
            val = math.inf
            best = None
            if (depth+self.game.startpos[1])%2:
                for move,child in n[CHILDREN]:
                    if val > child[PN]:
                        best = (move,child)
                        val = child[PN]
            else:
                for move,child in n[CHILDREN]:
                    if val > child[DN]:
                        best = (move,child)
                        val = child[DN]
            self.game.make_move(best[0])
            n = best[1]
            path.append(n)
            depth+=1
        return path,depth

    def evaluate(self, hashval, move, n, depth):
        if hashval in (self.provenset if depth<self.endgame_depth else self.endgame_provenset):
            return True
        if hashval in (self.disprovenset if depth<self.endgame_depth else self.endgame_disprovenset):
            return False
        if self.game.check_win(move):
            return (depth-1+self.game.startpos[1])%2
        if self.game.check_full():
            return self.drawproves
        return None

    def expand(self, n, depth):
        moves = self.game.get_actions()
        if len(moves)==0:
            n[PN]=0 if self.drawproves else math.inf
            n[DN]=math.inf if self.drawproves else 0
            return
        childdepth = depth+1
        myturn = (depth+self.game.startpos[1])%2
        use_ttable = self.ttable if childdepth<self.endgame_depth else self.ttable_endgame
        knownhashvals = set()
        for move in moves:
            self.game.make_move(move)
            hashval = self.game.basic_hash() if childdepth<self.endgame_depth else hash(self.game)
            if hashval in knownhashvals:
                self.game.revert_move(1)
                continue
            if hashval in use_ttable:
                found = use_ttable[hashval]
                found[PARENTS].append(n)
                n[CHILDREN].append((move,found))
                self.game.revert_move(1)
                continue
            knownhashvals.add(hashval)
            res = self.evaluate(hashval, move, n, childdepth)
            if res is None:
                child = [1,1,hashval,[n],[]]
                use_ttable[hashval]=child
            else:
                if res:
                    child = [0,math.inf]
                else:
                    child = [math.inf,0]
                if res!=myturn:
                    self.game.revert_move(1)
                    continue
            n[CHILDREN].append((move,child))
            self.node_count += 1
            if res==myturn:
                self.game.revert_move(1)
                break
            self.game.revert_move(1)

    def pn_search(self,depth=0):
        self.game.reset()
        if depth<self.endgame_depth:
            hashval = self.game.basic_hash()
            use_ttable = self.ttable
        else:
            hashval = hash(self.game)
            use_ttable = self.ttable_endgame
        self.root = [1,1,hashval,[],[]]
        self.node_count += 1
        use_ttable[hashval] = self.root
        curr_path = [self.root]
        c = 1
        while self.root[PN]!=0 and self.root[DN]!=0:
            if c % 1 == 0:
                #print(" ".join([str(x[1][PN]) for x in self.root[CHILDREN]]))
                #print(" ".join([str(x[1][DN]) for x in self.root[CHILDREN]]))
                if c % 1000000 == 0:
                    gc.collect()
                #print("Normal Proofadds: {}".format(self.proofadds))
                #print("Endgame Proofadds: {}".format(self.endgame_proofadds))
                if not util.resources_avaliable():
                    return False
            if c%100000==0:
                save_sets((self.provenset,self.prooffile),(self.disprovenset,self.disprooffile),
                          (self.endgame_provenset,self.endgame_prooffile),(self.endgame_disprovenset,self.endgame_disprooffile))
            c+=1
            path,depth = self.select_most_proving(curr_path[-1],depth)
            #draw_board(self.game.position,self.game.squares)
            curr_path = curr_path + path
            most_proving = curr_path[-1]
            self.expand(most_proving,depth)
            new_depth = self.update_anchestors(most_proving,depth)
            if new_depth < depth:
                self.game.revert_move(number=depth-new_depth)
                curr_path = curr_path[:new_depth-depth]
            depth = new_depth
        print(self.root[PN], self.root[DN], self.node_count)
        return True