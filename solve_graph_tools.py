import math
import util
import gc
import sys
from graph_tools_games import Tic_tac_toe
from graph_tools_game import Graph_game
from util import draw_board,check_position_consistent
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
GRAPH = 5 # A graph tools graph or None
PROOFNODE = 6 # Bool, are we in a proof node or disproof node

class PN_search():
    def __init__(self, game:Graph_game, drawproves=True,prooffile="provenset.txt",disprooffile="disprovenset.txt"):
        self.game = game
        self.startdepth = startdepth
        self.ttable = {}
        self.provenset = set()
        self.disprovenset = set()
        self.endgame_depth = endgame_depth
        self.node_count = 0
        self.proofadds = [0,0]
        self.endgame_proofadds = [0,0]
        self.drawproves = drawproves
        self.prooffile = prooffile
        self.disprooffile = disprooffile
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
        for _,c in ch:
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
        del n[CHILDREN]
        del n[PARENTS]
        # Do not use n aferwards
    
    def update_anchestors(self, n):
        #print(depth,n[HASH])
        old_pn = n[PN]
        old_dn = n[DN]
        self.set_pn_dn(n)
        if n[PN] == old_pn and n[DN] == old_dn and n[PN]!=0 and n[DN]!=0:
            return
        for p in n[PARENTS].copy():
            if len(p)>3:
                self.update_anchestors(p,depth-1)
        if (n[PN] == 0 or n[DN] == 0) and len(n)>PARENTS:
            self.delete_node(n, n[PARENTS], n[CHILDREN])

    def select_most_proving(self, n):
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
            n = best[1]
        return n

    def evaluate(self,hashval,graph:Graph):
        if hashval in self.provenset:
            return True
        elif hashval in self.disprovenset:
            return False
        elif graph.num_vertices()==0:
            return self.drawproves
        return None

    def expand(self, n):
        self.game.set_graph(Graph(n[GRAPH]))
        moves = self.game.get_actions()
        if moves is None:
            if n[PROOFNODE]:
                n[PN] = 0
                n[DN] = math.inf
            else:
                n[PN] = math.inf
                n[DN] = 0
            del n[GRAPH]
            del n[CHILDREN]
            return
        if len(moves)==0:
            raise Exception("No moves avaliable")
        knownhashvals = set()
        for move in moves:
            if move != moves[0]:
                if move == moves[-1]:
                    self.game.set_graph(n[GRAPH])
                else:
                    self.game.set_graph(Graph(n[GRAPH]))
            self.game.make_move(move)
            hashval = self.game.hash
            if hashval in knownhashvals:
                continue
            if hashval in self.ttable:
                found = self.ttable[hashval]
                found[PARENTS].append(n)
                n[CHILDREN].append(found)
                continue
            knownhashvals.add(hashval)
            res = self.evaluate(hashval,self.game.graph)
            if res is None:
                child = [1,1,hashval,[n],[],self.game.graph,not n[PROOFNODE]]
                self.ttable[hashval]=child
            else:
                if res:
                    if not n[PROOFNODE]:
                        continue
                    child = [0,math.inf]
                elif hashval in self.disprovenset:
                    if n[PROOFNODE]:
                        continue
                    child = [math.inf,0]
            n[CHILDREN].append(child)
            self.node_count += 1
            if res==n[PROOFNODE]:
                break
        n[GRAPH] = None

    def pn_search(self):
        hashval = self.game.hash
        self.root = [1,1,hashval,[],[],self.game.graph,True]
        self.node_count += 1
        self.ttable[hashval] = self.root
        c = 1
        times = {"select_most_proving":[],"expand":[],"update_anchestors":[],"whole_it":[]}
        starts = {}
        while self.root[PN]!=0 and self.root[DN]!=0:
            if c % 100 == 1:
                print("iteration:",c)
                for key,value in times.items():
                    print(key,np.mean(value))
                print(" ".join([str(x[PN]) for x in self.root[CHILDREN]]))
                print(" ".join([str(x[DN]) for x in self.root[CHILDREN]]))
                if c % 1000000 == 0:
                    gc.collect()
                print("Normal Proofadds: {}".format(self.proofadds))
                print("Endgame Proofadds: {}".format(self.endgame_proofadds))
                if not util.resources_avaliable():
                    return False
            if c%100000==0:
                save_sets((self.provenset,self.prooffile),(self.disprovenset,self.disprooffile),
                          (self.endgame_provenset,self.endgame_prooffile),(self.endgame_disprovenset,self.endgame_disprooffile))
            starts["whole_it"] = time.perf_counter()
            c+=1
            starts["select_most_proving"] = time.perf_counter()
            most_proving = self.select_most_proving(self.root)
            times["select_most_proving"].append(time.perf_counter()-starts["select_most_proving"])
            starts["expand"] = time.perf_counter()
            self.expand(most_proving)
            times["expand"].append(time.perf_counter()-starts["expand"])
            starts["update_anchestors"] = time.perf_counter()
            self.update_anchestors(most_proving)
            times["update_anchestors"].append(time.perf_counter()-starts["update_anchestors"])
            times["whole_it"].append(time.perf_counter()-starts["whole_it"])
        print(self.root[PN], self.root[DN], self.node_count)
        return True