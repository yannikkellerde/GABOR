import math
from tic_tac_toe import Tic_tac_toe
import util
import gc
import sys
import logging
from data_magic import save_sets

logging.basicConfig(filename='solver.log', filemode='w', level=logging.INFO)

def reconstruct_vicory(game, provenset):
    def recurso(node):
        game.set_state(node.position, node.myturn)
        moves = game.get_actions()
        if node.myturn:
            for move in moves:
                game.set_state(node.position, node.myturn)
                game.make_move(move)
                hashval = game.hashpos()
                if hashval in provenset or game.check_win(move):
                    child = Node(game.onturn, game.position, node, 0, math.inf)
                    node.children.append(child)
                    if hashval in provenset:
                        recurso(child)
                    return
        else:
            for move in moves:
                game.set_state(node.position, node.myturn)
                game.make_move(move)
                child = Node(game.onturn, game.position, node, 0, math.inf)
                node.children.append(child)
                recurso(child)
    node = Node(game.onturn, game.position, None, 0, math.inf)
    node.parents = []
    recurso(node)
    return node

class Node():
    def __init__(self, myturn, position, parent, pn, dn):
        self.myturn = myturn
        self.position = position
        self.pn = pn
        self.dn = dn
        self.children = []
        self.parents = [parent]

class Mininode():
    def __init__(self, pn, dn):
        self.pn = pn
        self.dn = dn

class PN_DAG():
    def __init__(self, game, drawproves=True,prooffile="provenset.txt",disprooffile="disprovenset.txt"):
        self.game = game
        self.ttable = {}
        self.provenset = set()
        self.disprovenset = set()
        self.node_count = 0
        self.proofadds = [0,0]
        self.drawproves = drawproves
        self.prooffile = prooffile
        self.disprooffile = disprooffile

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
        if n.pn == 0 or n.dn == 0:
            return
        if n.myturn:
            n.pn = math.inf; n.dn = 0
            for c in n.children:
                n.dn += c.dn
                n.pn = min(n.pn, c.pn)
        else:
            n.dn = math.inf; n.pn = 0
            for c in n.children:
                n.pn += c.pn
                n.dn = min(n.dn, c.dn)

    def delete_node(self, n, ps, ch):
        for p in ps:
            p.children.remove(n)
        for c in ch:
            if isinstance(c, Node):
                c.parents.remove(n)
                if len(c.parents)==0:
                    self.delete_node(c, [], c.children[:])
        self.game.set_state(n.position, n.myturn)
        hashval = self.game.hashpos()
        del self.ttable[hashval]
        n.children = []
        n.parents = []
        if n.pn == 0:
            self.proofadds[0] += 1
            self.provenset.add(hashval)
        elif n.dn == 0:
            self.proofadds[1] += 1
            self.disprovenset.add(hashval)

    def update_anchestors(self, n):
        old_pn = n.pn
        old_dn = n.dn
        self.set_pn_dn(n)
        if n.pn == old_pn and n.dn == old_dn and n.pn!=0 and n.dn!=0:
            return
        ps = n.parents[:]
        if n.position == (4296289024, 50872372):
            for child in n.children:
                if child.pn == 0:
                    print(child.position)
        for p in ps:
            self.update_anchestors(p)
        if (n.pn == 0 or n.dn == 0) and len(n.parents)>0:
            self.delete_node(n, n.parents, n.children)

    def select_most_proving(self, n):
        depth = 0
        while n.children:
            val = math.inf
            best = None
            if n.myturn or depth==0:
                for c in n.children:
                    if val > c.pn:
                        best = c
                        val = c.pn
            else:
                for c in n.children:
                    if val > c.dn:
                        best = c
                        val = c.dn
            n = best
            depth += 1
        return n

    def evaluate(self, hashval, move, n):
        if hashval in self.provenset:
            return True
        if hashval in self.disprovenset:
            return False
        if self.game.check_win(move):
            return n.myturn
        if self.game.check_full():
            return self.drawproves
        return None

    def expand(self, n):
        self.game.set_state(n.position, n.myturn)
        moves = self.game.get_actions()
        if len(moves)==0:
            n.pn=0 if self.drawproves else math.inf
            n.dn=math.inf if self.drawproves else 0
            return
        for move in moves:
            self.game.make_move(move)
            hashval = self.game.hashpos()
            if hashval in self.ttable:
                found = self.ttable[hashval]
                if not found in n.children:
                    found.parents.append(n)
                    n.children.append(found)
                self.game.set_state(n.position, n.myturn)
                continue
            res = self.evaluate(hashval, move, n)
            if res is None:
                child = Node(self.game.onturn, tuple(self.game.position), n, 1, 1)
                self.ttable[hashval]=child
            else:
                if res:
                    child = Mininode(0, math.inf)
                else:
                    child = Mininode(math.inf, 0)
                if res!=n.myturn:
                    self.game.set_state(n.position, n.myturn)
                    continue
            n.children.append(child)
            self.node_count += 1
            if res==n.myturn:
                break
            self.game.set_state(n.position, n.myturn)
    def pn_search(self):
        self.game.reset()
        self.root = Node(self.game.onturn, tuple(self.game.position), None, 1, 1)
        self.root.parents = []
        self.node_count += 1
        self.ttable[self.game.hashpos()] = self.root
        # util.buildupnodestruct(Node, [1<<2, 1<<12], self.root, self.game, self.ttable)
        # util.buildupnodestruct(Node,[1<<8, 1<<15, 1<<14, 1<<13, 1<<28],self.root,self.game,self.ttable)
        c = 1
        while self.root.pn!=0 and self.root.dn!=0:
            if c % 1000 == 0:
                print(self.node_count, " ".join([str(x.pn) for x in self.root.children]))
                print(self.node_count, " ".join([str(x.dn) for x in self.root.children]))
                if c % 1000000 == 0:
                    gc.collect()
                print("Proofadds: {}".format(self.proofadds))
                #tracked_nodes = list(filter(lambda x:isinstance(x,Node), gc.get_objects()))
                #print("Tracked nodes: {}, in ttable: {}, deletions: {}".format(len(tracked_nodes),len(self.ttable),self.deletions))
                """for item in tracked_nodes:
                    self.game.set_state(item.position, item.myturn)
                    hashval = self.game.hashpos()
                    if hashval not in self.ttable:
                        g = gc.get_referrers(item)
                        print(g)"""
                if not util.resources_avaliable():
                    return False
            if c%100000==0:
                save_sets(self.provenset,self.disprovenset,prooffile=self.prooffile,disprooffile=self.disprooffile)
            c+=1
            most_proving = self.select_most_proving(self.root)
            self.expand(most_proving)
            self.update_anchestors(most_proving)
        print(self.root.pn, self.root.dn, self.node_count)
        return True