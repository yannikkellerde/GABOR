import math
from tqdm import tqdm,trange
from copy import copy,deepcopy
from functools import reduce
from collections import defaultdict
import time
import numpy as np
import pickle
import matplotlib.pyplot as plt
from board_representation import Board_game

from graph_tool.all import *
from graph_tools_hashing import wl_hash

class Graph_game():
    graph: Graph
    board:Board_game
    def __init__(self):
        self.hashme()
        self.owner_map = {0:None,1:"f",2:"b",3:"w"}
        self.owner_rev = {val:key for key,val in self.owner_map.items()}

    @property
    def hash(self):
        return self.graph.gp["h"]

    @property
    def onturn(self):
        return "b" if self.graph.gp["b"] else "w"

    def hashme(self):
        wl_hash(self.graph,self.graph.vp.o,iterations=3)

    def graph_from_board(self):
        self.graph = Graph(directed=False)
        self.graph.gp["h"] = self.graph.new_graph_property("long")
        self.graph.gp["b"] = self.graph.new_graph_property("bool")
        self.graph.gp["b"] = True if self.board.onturn=="b" else False
        owner_prop = self.graph.new_vertex_property("short")
        self.graph.vp.o = owner_prop
        hash_prop = self.graph.new_vertex_property("long")
        self.graph.vp.h = hash_prop
        added_verts = dict()
        for i,wsn in enumerate(list(self.board.winsquarenums)):
            owner = self.owner_rev["f"]
            add_verts = []
            for ws in wsn:
                if self.board.position[ws] == "f":
                    add_verts.append(ws)
                if self.board.position[ws] != self.owner_map[owner]:
                    if self.owner_map[owner] == "f":
                        owner = self.owner_rev[self.board.position[ws]]
                    else:
                        break
            else:
                ws_vert = self.graph.add_vertex()
                self.graph.vp.o[ws_vert] = owner
                for av in add_verts:
                    if av in added_verts:
                        my_v = added_verts[av]
                    else:
                        my_v = self.graph.add_vertex()
                        self.graph.vp.o[my_v] = 0
                        added_verts[av] = my_v
                    self.graph.add_edge(ws_vert,my_v)
        self.hashme()

    def set_graph(self,G:Graph):
        self.graph = G
        self.hashme()

    def get_actions(self):
        actions = []
        for node in self.graph.vertices():
            if self.graph.vp.o[node]!=0:
                continue
            left_to_own = 0
            go_there = False
            for target in node.all_neighbors():
                count = target.out_degree()
                if count==1:
                    if self.owner_map[self.graph.vp.o[node]] == self.onturn:
                        return None
                    go_there = True
                left_to_own += count
            actions.append((-10000*int(go_there)-node.degree()*3+left_to_own,self.graph.vp.h[node]))
        actions.sort()
        return [x[1] for x in actions]
    
    def make_move(self,move):
        win = False
        square_node, = find_vertex(self.graph,self.graph.vp.h,move)
        del_nodes = [square_node]
        lost_neighbors = defaultdict(int)
        for wp_node in square_node.neighbors():
            owner = self.owner_map(self.graph.vp.o[wp_node])
            if owner == "f":
                self.graph.vp.o[wp_node] = self.onturn
            elif owner == self.onturn:
                if wp_node.degree == 1:
                    win = True
            else:
                for sq_node in wp_node.neighbors():
                    i = self.graph.vertex_index[sq_node]
                    if sq_node.degree() - lost_neighbors[i] == 1:
                        del_nodes.append(sq_node)
                del_nodes.append(wp_node)
        self.graph.remove_vertex(del_nodes)
        self.graph.gp["b"] = not self.graph.gp["b"]
        self.hashme()
        return win

    def draw_me(self):
        fill_color = self.graph.new_vertex_property("vector<float>")
        fill_color.a = [(0,0,1,1) if x==0 else ((0,1,1,1) if x==1 else ((0,0,0,1) if x==2 else (255,0,0,1))) for x in self.graph.vp.o.a]
        graph_draw(self.graph, vprops={"fill_color":fill_color} vertex_text=self.graph.vertex_index, output="game_state.pdf")