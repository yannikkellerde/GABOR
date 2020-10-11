import math
from tqdm import tqdm,trange
from copy import copy,deepcopy
from functools import reduce
from collections import defaultdict
import time
import numpy as np
import pickle
import matplotlib.pyplot as plt
from graph_board_game import Board_game

from graph_tool.all import *
from graph_tools_hashing import wl_hash

class Graph_game():
    graph: Graph
    board:Board_game
    def __init__(self):
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
                elif self.board.position[ws] != self.owner_map[owner]:
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
                        self.board.node_map[my_v] = av
                        self.graph.vp.o[my_v] = 0
                        added_verts[av] = my_v
                    self.graph.add_edge(ws_vert,my_v)
        self.hashme()

    def set_graph(self,G:Graph):
        self.graph = G
        self.hashme()

    def get_actions(self):
        actions = []
        alreadys = set()
        for node in self.graph.vertices():
            if self.graph.vp.o[node]!=0:
                continue
            left_to_own = 0
            go_there = False
            neigh_indices = set()
            for target in node.all_neighbors():
                neigh_indices.add(int(target))
                count = target.out_degree()
                if count==1:
                    if self.owner_map[self.graph.vp.o[target]] == self.onturn:
                        return None
                    go_there = True
                left_to_own += count
            if self.graph.vp.h[node] not in alreadys:
                alreadys.add(self.graph.vp.h[node])
                deg = node.out_degree()
                actions.append((-10000*int(go_there)-deg+left_to_own/deg,self.graph.vp.h[node],neigh_indices))
        actions.sort()
        # Remove superseeded actions
        for i in range(len(actions)-1,-1,-1):
            for j in range(i-1,-1,-1):
                if actions[i][2].issubset(actions[j][2]):
                    del actions[i]
                    break
        return [x[1] for x in actions]
    
    def make_move_vertex(self,square_node):
        del_nodes = [square_node]
        lost_neighbors = defaultdict(int)
        for wp_node in square_node.all_neighbors():
            owner = self.owner_map[self.graph.vp.o[wp_node]]
            if owner == "f":
                self.graph.vp.o[wp_node] = self.owner_rev[self.onturn]
            elif owner != self.onturn:
                for sq_node in wp_node.all_neighbors():
                    i = self.graph.vertex_index[sq_node]
                    if sq_node.out_degree() - lost_neighbors[i] == 1:
                        del_nodes.append(sq_node)
                    lost_neighbors[i]+=1
                del_nodes.append(wp_node)
        del_inds = [int(x) for x in del_nodes]
        self.graph.remove_vertex(del_nodes,fast=True)
        self.graph.gp["b"] = not self.graph.gp["b"]
        return del_inds

    def track_vertex(self,vert_index,del_inds):
        if vert_index<self.graph.num_vertices():
            if vert_index in del_inds:
                raise Exception("Can't track deleted vertex")
            return vert_index
        ind_list = list(range(self.graph.num_vertices()))
        for ind in sorted(del_inds):
            if ind==len(ind_list):
                ind_list.append(None)
            else:
                ind_list.append(ind_list[ind])
                ind_list[ind] = None
        return ind_list[vert_index]

    def make_move(self,move,hashme=True):
        square_node = list(find_vertex(self.graph,self.graph.vp.h,move))[0]
        self.make_move_vertex(square_node)
        if hashme:
            self.hashme()

    def forced_move_search(self):
        moves = set()
        vert_inds = dict()
        double_threat = set()
        force_me_to = None
        loss = False
        for vert in self.graph.vertices():
            deg = vert.out_degree()
            owner = self.owner_map[self.graph.vp.o[vert]]
            if owner != None:
                if owner == self.onturn or owner=="f":
                    if deg == 1:
                        return True
                    elif deg == 2:
                        nod1,nod2 = vert.all_neighbors()
                        ind1,ind2 = int(nod1),int(nod2)
                        if ind1 in vert_inds:
                            double_threat.add(ind1)
                        if ind2 in vert_inds:
                            double_threat.add(ind2)
                        vert_inds[ind1] = ind2
                        vert_inds[ind2] = ind1
                else:
                    if deg == 1:
                        sq, = vert.all_neighbors()
                        ind = self.graph.vertex_index[sq]
                        if force_me_to is None:
                            force_me_to = ind
                        else:
                            if ind != force_me_to:
                                loss = True
        if loss:
            return False
        if force_me_to is not None:
            if force_me_to in vert_inds:
                vert_inds = {force_me_to:vert_inds[force_me_to]}
            else:
                return None
        if len(set(vert_inds).intersection(double_threat))>0:
            return True
        if len(vert_inds) > 1:
            orig_graph = Graph(self.graph)
        for i,ind in enumerate(vert_inds.keys()):
            if i!=0:
                if i==len(vert_inds)-1:
                    self.graph = orig_graph
                else:
                    self.graph = Graph(orig_graph)
            vert = self.graph.vertex(ind)
            del_inds = self.make_move_vertex(vert)
            reply_ind = self.track_vertex(vert_inds[ind],del_inds)
            reply_vert = self.graph.vertex(reply_ind)
            self.make_move_vertex(reply_vert)
            if self.forced_move_search():
                return True
        return None

    def draw_me(self,index=0):
        if self.graph.num_vertices()==0:
            print("WARNING: Trying to draw graph without vertices")
            return
        fill_color = self.graph.new_vertex_property("vector<float>")
        for vertex in self.graph.vertices():
            x = self.graph.vp.o[vertex]
            fill_color[vertex] = (0,0,1,1) if x==0 else ((0,1,1,1) if x==1 else ((0,0,0,1) if x==2 else (255,0,0,1)))
        graph_draw(self.graph, vprops={"fill_color":fill_color}, vertex_text=self.graph.vertex_index, output=f"game_state_{index}.pdf")