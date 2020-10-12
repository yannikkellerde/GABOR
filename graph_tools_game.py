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
        self.board.node_map = dict()
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
                        self.board.node_map[int(my_v)] = av
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
        del_inds = set(int(x) for x in del_nodes)
        self.graph.remove_vertex(del_nodes,fast=True)
        self.graph.gp["b"] = not self.graph.gp["b"]
        return del_inds

    def track_vertices(self,del_inds):
        ind_list = list(range(self.graph.num_vertices()))
        for ind in sorted(del_inds):
            if ind==len(ind_list):
                ind_list.append(None)
            else:
                ind_list.append(ind_list[ind])
                ind_list[ind] = None
        return ind_list
    
    def track_forward(self,del_inds,ind_list):
        for ind in reversed(sorted(del_inds)):
            if ind != len(ind_list)-1:
                ind_list[ind] = ind_list.pop()
            else:
                ind_list.pop()

    def negate_onturn(self,onturn):
        return "b" if onturn=="w" else ("w" if onturn=="b" else onturn)
        
    def threat_search(self,last_gain=None,last_cost=None,known_threats=dict(),gain=set(),cost=set()):
        legit_defenses = set()
        movelines = []
        winlines = []
        force_me_to = None
        vert_inds = dict()
        double_threat = dict()
        done = False
        if last_gain is None:
            for vert in self.graph.vertices():
                deg = vert.out_degree()
                owner = self.owner_map[self.graph.vp.o[vert]]
                if owner != None:
                    if owner == self.onturn or owner=="f":
                        if deg == 1:
                            sq, = neigh
                            use_defenses = set()
                            use_defenses.add(sq)
                            winlines.append(use_defenses)
                            movelines.append([last_gain,sq,"deg1"])
                            done = True
                            break
                        elif deg == 2:
                            nod1,nod2 = vert.all_neighbors()
                            ind1,ind2 = int(nod1),int(nod2)
                            if ind1 in vert_inds:
                                double_threat[ind1]=(ind2,vert_inds[ind1])
                            if ind2 in vert_inds:
                                double_threat[ind2] = (ind1,vert_inds[ind2])
                            vert_inds[ind1] = ind2
                            vert_inds[ind2] = ind1
                    else:
                        if deg == 1:
                            sq, = vert.all_neighbors()
                            ind = self.graph.vertex_index[sq]
                            if force_me_to is None:
                                force_me_to = ind
                                legit_defenses.add(int(sq))
                            else:
                                if ind != force_me_to:
                                    done = True
                        elif deg == 2:
                            sq1,sq2 = vert.all_neighbors()
                            legit_defenses.add(int(sq1))
                            legit_defenses.add(int(sq2))
        else:
            rest_squares = set()
            for wp_ind in self.graph.get_all_neighbors(last_cost):
                vert = self.graph.vertex(wp_ind)
                if self.owner_map[self.graph.vp.o[vert]] == self.onturn:
                    continue
                frees = set()
                for sq_ind in self.graph.get_all_neighbors(wp_ind):
                    if sq_ind in gain:
                        break
                    if sq_ind not in cost:
                        frees.add(sq_ind)
                else:
                    if len(frees)==1:
                        force_me_to, = frees
                        legit_defenses.add(force_me_to)
                    elif len(frees)==2:
                        for f in frees:
                            legit_defenses.add(f)
            for wp_ind in self.graph.get_all_neighbors(last_gain):
                vert = self.graph.vertex(wp_ind)
                if self.owner_map[self.graph.vp.o[vert]] == self.negate_onturn(self.onturn):
                    continue
                frees = set()
                for sq_ind in self.graph.get_all_neighbors(wp_ind):
                    if sq_ind in cost:
                        break
                    if sq_ind not in gain:
                        frees.add(sq_ind)
                else:
                    if len(frees) == 1:
                        sq, = frees
                        use_defenses = set()
                        use_defenses.add(sq)
                        winlines.append(use_defenses)
                        movelines.append([last_gain,sq,"deg1_inner"])
                        done = True
                    elif len(frees) == 2:
                        ind1,ind2 = frees
                        if ind1 in vert_inds:
                            double_threat[ind1]=(ind2,vert_inds[ind1])
                        if ind2 in vert_inds:
                            double_threat[ind2]=(ind1,vert_inds[ind2])
                        vert_inds[ind1] = ind2
                        vert_inds[ind2] = ind1
                    else:
                        rest_squares.update(frees)
            for key in known_threats:
                if key in rest_squares and not key in cost and not key in gain and not known_threats[key] in cost:
                    vert_inds[key] = known_threats[key]
        if not done:
            if force_me_to is not None:
                if force_me_to in vert_inds:
                    vert_inds = {force_me_to:vert_inds[force_me_to]}
                else:
                    done = True
        if not done:
            for n in set(vert_inds).intersection(set(double_threat)):
                use_defenses = legit_defenses.copy()
                use_defenses.add(double_threat[n][0])
                use_defenses.add(double_threat[n][1])
                use_defenses.add(n)
                winlines.append(use_defenses)
                movelines.append([last_gain,n,"double_threat"])
                done = True
        if not done:
            known_threats.update(vert_inds)
            for i,ind in enumerate(vert_inds.keys()):
                use_cost = cost.copy()
                use_gain = gain.copy()
                use_cost.add(vert_inds[ind])
                use_gain.add(ind)
                th_copy = known_threats.copy()
                del th_copy[ind]
                under_defs,win_here,move_here = self.threat_search2(last_gain=ind,last_cost=vert_inds[ind],gain=use_gain,cost=use_cost,known_threats=th_copy)
                if win_here:
                    for move in move_here:
                        movelines.append([last_gain]+move)
                    under_defs.update(legit_defenses)
                    under_defs.add(ind)
                    under_defs.add(vert_inds[ind])
                    winlines.append(under_defs)
        if len(winlines)>0:
            return reduce(lambda x,y:x.intersection(y),winlines), True, movelines
        else:
            return set(), False, []

    def make_move(self,move,hashme=True):
        square_node = list(find_vertex(self.graph,self.graph.vp.h,move))[0]
        self.make_move_vertex(square_node)
        if hashme:
            self.hashme()

    def forced_move_search(self):
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
            reply_ind = self.track_vertices(del_inds)[vert_inds[ind]]
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