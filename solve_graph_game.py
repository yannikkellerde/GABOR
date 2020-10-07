import math
import sys
from graph_games import Tic_tac_toe
import numpy as np
import time
from graph_tool.all import *

class PN_search():
    def __init__(self):
        self.graph = Graph()
        self.game = Tic_tac_toe()
        self.root = self.graph.add_vertex()
        self.graph.vp.pn = self.graph.new_vertex_property("int")
        self.graph.vp.dn = self.graph.new_vertex_property("int")
        self.graph.vp.hash = self.graph.new_vertex_property("long")
        self.pn = self.graph.vp.pn
        self.dn = self.graph.vp.dn
        self.hash = self.graph.vp.hash
        self.pn[self.root] = 1
        self.dn[self.root] = 1
        self.hash[self.root] = self.game.hash
        self.ttable = {}
        self.provenset = set()
        self.disprovenset = set()
        self.prooffile = "provenset.txt"
        self.disprooffile = "disprovenset.text"
    
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

    def set_pn_dn(self,vertex,is_prove_node):
        if self.pn[vertex]==0 or self.dn[vertex]==0:
            return
        if is_prove_node:
            self.pn[vertex] = math.inf;self.dn[vertex]=0
            for child in vertex.out_neighbors():
                self.dn[vertex] += self.dn[child]
                self.pn[vertex] = min(self.pn[vertex], self.pn[child])
        else:
            self.dn[vertex] = math.inf;self.pn[vertex]=0
            for child in vertex.out_neighbors():
                self.pn[vertex] += self.pn[child]
                self.dn[vertex] = min(self.dn[vertex], self.dn[child])

    def delete_node(self, vertex, is_prove_node):
        parents = list(vertex.in_neighbors())
        children = list(vertex.out_neighbors())
        del self.ttable[self.hash[vertex]]
        for c in children:
            
        self.graph.remove_vertex(vertex,fast=True)