import math
from util import resources_avaliable,draw_pn_tree
import gc
import pickle
import os,sys
from graph_tools_games import Tic_tac_toe,Qango6x6
from graph_tools_game import Graph_game
from data_magic import save_sets
from graph_tool.all import *
import numpy as np
import time

# Node storage for memory efficency in lists
PN = 0 # int
DN = 1 # int
HASH = 2 # int
PARENTS = 3 # List of Nodes(which are lists)
CHILDREN = 4 # List of tuples containing move made and Node (which is a lists)
PROOFNODE = 5 # Bool, are we in a proof node or disproof node
STORAGE = 6 # A tuple containing 1. an owner map, 2. a filter map, 3. onturn bool


class PN_search():
    def __init__(self, game:Graph_game, drawproves=False,prooffile="proofsets/provenset.pkl",disprooffile="proofsets/disprovenset.pkl"):
        self.game = game
        self.ttable = {}
        self.provenset = set()
        self.disprovenset = set()
        self.node_count = 0
        self.alive_graphs = 0
        self.proofadds = [0,0]
        self.drawproves = drawproves
        self.prooffile = prooffile
        self.disprooffile = disprooffile
        os.makedirs(os.path.dirname(self.prooffile),exist_ok=True)
        self.loadsets()

    def loadsets(self):
        try:
            with open(self.prooffile,"rb") as file:
                self.provenset = pickle.load(file)
        except Exception as e:
            print(e)
        try:
            with open(self.disprooffile,"rb") as file:
                self.disprovenset = pickle.load(file)
        except Exception as e:
            print(e)
    
    def set_pn_dn(self, n):
        if n[PN] == 0 or n[DN] == 0:
            return
        if n[PROOFNODE]:
            n[PN] = math.inf; n[DN] = 0
            for c in n[CHILDREN]:
                n[DN] += c[DN]
                n[PN] = min(n[PN], c[PN])
        else:
            n[DN] = math.inf; n[PN] = 0
            for c in n[CHILDREN]:
                n[PN] += c[PN]
                n[DN] = min(n[DN], c[DN])

    def delete_node(self, n, ps, ch):
        for p in ps:
            for i in range(len(p[CHILDREN])):
                if p[CHILDREN][i]==n:
                    del p[CHILDREN][i]
                    break
        for c in ch:
            if len(c)>PARENTS:
                c[PARENTS].remove(n)
                if len(c[PARENTS])==0:
                    self.delete_node(c, [], c[CHILDREN].copy())
        del self.ttable[n[HASH]]
        if n[PN] == 0:
            self.provenset.add(n[HASH])
            self.proofadds[0] += 1
        elif n[DN] == 0:
            self.disprovenset.add(n[HASH])
            self.proofadds[1] += 1
        if len(n)>STORAGE:
            self.alive_graphs-=1
            del n[STORAGE]
        del n[PROOFNODE]
        del n[CHILDREN]
        del n[PARENTS]
        # Do not use n aferwards
    
    def update_anchestors(self, n):
        old_pn = n[PN]
        old_dn = n[DN]
        self.set_pn_dn(n)
        if n[PN] == old_pn and n[DN] == old_dn and n[PN]!=0 and n[DN]!=0:
            return
        for p in n[PARENTS].copy():
            if len(p)>3:
                self.update_anchestors(p)
        if (n[PN] == 0 or n[DN] == 0) and len(n)>PARENTS:
            self.delete_node(n, n[PARENTS], n[CHILDREN])

    def select_most_proving(self, n):
        depth = 0
        while n[CHILDREN]:
            val = math.inf
            best = None
            if n[PROOFNODE]:
                for child in n[CHILDREN]:
                    if val > child[PN]:
                        best = child
                        val = child[PN]
            else:
                for child in n[CHILDREN]:
                    if val > child[DN]:
                        best = child
                        val = child[DN]
            n = best
            depth += 1
        return n,depth

    def evaluate(self,n,hashval):
        if hashval in self.provenset:
            return True
        elif hashval in self.disprovenset:
            return False
        elif self.game.view.num_vertices()==0:
            return self.drawproves
        return None

    def expand(self, n, threat_search=True, blocked_moves=None):
        self.game.load_storage(n[STORAGE])
        moves = self.game.get_actions()
        if moves is None:
            if n[PROOFNODE]:
                n[PN] = 0
                n[DN] = math.inf
            else:
                n[PN] = math.inf
                n[DN] = 0
            del n[STORAGE]
            return
        if len(moves)==0:
            if self.drawproves:
                n[PN] = 0
                n[DN] = math.inf
            else:
                n[PN] = math.inf
                n[DN] = 0
            del n[STORAGE]
            return
        if blocked_moves is not None:
            moves = [move for move in moves if move not in blocked_moves]
        if threat_search:
            self.game.view.gp["b"] = not self.game.view.gp["b"]
            defense_vertices,has_threat,_ = self.game.threat_search()
            self.game.view.gp["b"] = not self.game.view.gp["b"]
            if has_threat:
                moves = [move for move in moves if move in defense_vertices]
        knownhashvals = set()
        for move in moves:
            if move != moves[0]:
                self.game.load_storage(n[STORAGE])
            self.game.make_move(move)
            self.game.hashme()
            hashval = self.game.hash
            if hashval in knownhashvals:
                continue
            if hashval in self.ttable:
                found = self.ttable[hashval]
                found[PARENTS].append(n)
                n[CHILDREN].append(found)
                continue
            knownhashvals.add(hashval)
            res = self.evaluate(n,hashval)
            if res is None:
                child = [1,1,hashval,[n],[],not n[PROOFNODE],self.game.extract_storage()]
                self.alive_graphs += 1
                self.ttable[hashval]=child
            else:
                if res:
                    if not n[PROOFNODE]:
                        continue
                    child = [0,math.inf]
                else:
                    if n[PROOFNODE]:
                        continue
                    child = [math.inf,0]
            n[CHILDREN].append(child)
            self.node_count += 1
            if res==n[PROOFNODE]:
                break
        del n[STORAGE]
        self.alive_graphs -= 1

    def pn_search(self,onturn_proves=True,verbose=True,save=True,burgregel=2):
        self.game.hashme()
        hashval = self.game.hash
        self.root = [1,1,hashval,[],[],onturn_proves,self.game.extract_storage()]
        if burgregel in [1,2]:
            blocked = self.game.board.get_burgregel_blocked()
        elif burgregel == 3:
            blocked = self.game.board.get_profiregel_blocked()
        self.alive_graphs+=1
        self.node_count += 1
        self.ttable[hashval] = self.root
        c = 1
        times = {"select_most_proving":[],"expand":[],"update_anchestors":[],"whole_it":[]}
        starts = {}
        while self.root[PN]!=0 and self.root[DN]!=0:
            if verbose:
                if c % 100 == 1:
                    print("iteration:",c)
                    print("node_count:",self.node_count)
                    print("graphs:",self.alive_graphs)
                    for key,value in times.items():
                        print(key,np.mean(value))
                    cur = self.root
                    depth = 0
                    while len(cur[CHILDREN]) == 1:
                        cur = cur[CHILDREN][0]
                        depth += 1
                    print("depth:",depth)
                    print(" ".join([str(x[PN]) for x in cur[CHILDREN]]))
                    print(" ".join([str(x[DN]) for x in cur[CHILDREN]]))
                    if c % 1000000 == 0:
                        gc.collect()
                    print("Proofadds: {}".format(self.proofadds))
                    if not resources_avaliable():
                        return False
                    times = {"select_most_proving":[],"expand":[],"update_anchestors":[],"whole_it":[]}
            if save:
                if c%10000==0:
                    save_sets((self.provenset,self.prooffile),(self.disprovenset,self.disprooffile))
                    draw_pn_tree(self.root,2)
            starts["whole_it"] = time.perf_counter()
            c+=1
            starts["select_most_proving"] = time.perf_counter()
            most_proving,depth = self.select_most_proving(self.root)
            times["select_most_proving"].append(time.perf_counter()-starts["select_most_proving"])
            starts["expand"] = time.perf_counter()
            if burgregel==0:
                self.expand(most_proving)
            elif burgregel==1 or burgregel==3:
                if depth==0:
                    self.expand(most_proving,blocked_moves=blocked)
                else:
                    self.expand(most_proving)
            elif burgregel==2:
                if depth==0 or depth==2:
                    self.expand(most_proving,blocked_moves=blocked)
                elif depth==1:
                    self.expand(most_proving,threat_search=False)
                else:
                    self.expand(most_proving)
            times["expand"].append(time.perf_counter()-starts["expand"])
            starts["update_anchestors"] = time.perf_counter()
            self.update_anchestors(most_proving)
            times["update_anchestors"].append(time.perf_counter()-starts["update_anchestors"])
            times["whole_it"].append(time.perf_counter()-starts["whole_it"])
        if verbose:
            print("iteration:",c)
            print("node_count:",self.node_count)
            print("graphs:",self.alive_graphs)
            print("Proofadds: {}".format(self.proofadds))
            print(self.root[PN], self.root[DN], self.node_count)
        if save:
            save_sets((self.provenset,self.prooffile),(self.disprovenset,self.disprooffile))
        return True


if __name__ == "__main__":
    g = Qango6x6()
    burgregel = 3
    pn_s = PN_search(g,prooffile=f"proofsets/burgregel{burgregel}p.pkl",disprooffile=f"proofsets/burgregel{burgregel}d.pkl")
    pn_s.pn_search(onturn_proves=True,burgregel=burgregel)