import math
from tqdm import tqdm,trange
from copy import copy,deepcopy
from functools import reduce
import time
import numpy as np
import pickle
import networkx as nx
import matplotlib.pyplot as plt
from orderedset import OrderedSet

from graph_hashing import wl_hash

class Graph_game():
    graph: nx.Graph
    startgraph: nx.Graph
    def __init__(self):
        self.hashme()
        self.startgraph = self.graph.copy()
        self.revert_history = []
        self.random_pos = nx.random_layout(self.graph, seed=42)

    @property
    def hash(self):
        return self.graph.graph["hash"]

    @property
    def onturn(self):
        return self.graph.graph["onturn"]

    def change_attrib(self,node,attrib,value):
        self.graph.nodes[node][attrib] = value
    
    def change_graph_attrib(self,attrib,value):
        self.graph.graph[attrib] = value

    def get_node_attribs(self):
        return dict(self.graph.nodes(data=True))
    
    def write_node_attribs(self,node_attribs):
        for key,value in node_attribs.items():
            self.graph.add_node(key,**value)

    def hashme(self):
        wl_hash(self.graph,edge_attr="color",node_attr="owner",iterations=3)

    def reset(self):
        self.graph = self.startgraph.copy()

    def revert_moves(self,amount):
        for _ in range(amount):
            if len(self.revert_history)==0:
                self.hashme()
                return False
            instructions = self.revert_history.pop()
            for func,args,kwargs in instructions:
                func(*args,**kwargs)
        return True
    
    def get_actions(self):
        alreadymaps = {}
        for node,nattribs in self.graph.nodes(data=True):
            toadd = None
            blue_neighbours = 0
            for target,eattribs in self.graph.adj[node].items():
                if eattribs["color"] == "g":
                    if target in alreadymaps:
                        toadd = target
                else:
                    blue_neighbours += 1
            if blue_neighbours == 0 and nattribs["owner"] == self.graph.graph["onturn"]:
                return None
            if toadd is None:
                alreadymaps[node] = [blue_neighbours,blue_neighbours==0,[nattribs["label"]]]
            else:
                alreadymaps[toadd][2].append(nattribs["label"])
                if blue_neighbours == 0:
                    alreadymaps[toadd][1] = True
                alreadymaps[toadd][0] += blue_neighbours
        actions = list(OrderedSet([frozenset(x[2]) for x in sorted(alreadymaps.values(),key=lambda x:-10000*int(x[1])-len(x[2])*100+x[0])]))
        return actions
    
    def make_move(self,move):
        revert_instructions = []
        revert_instructions.append((self.write_node_attribs,(self.get_node_attribs(),),{}))
        win = False
        for node,nattribs in self.graph.nodes(data=True):
            if nattribs["label"] in move:
                nodes = {(node,nattribs["owner"])}
                labels = {nattribs["label"]}
                for target,eattribs in self.graph.adj[node].items():
                    tattribs = self.graph.nodes[target]
                    if eattribs["color"]=="g":
                        if tattribs["label"] in move:
                            nodes.add((target,tattribs["owner"]))
                            labels.add(tattribs["label"])
                        else:
                            break
                else:
                    if labels==move:
                        break
        else:
            raise Exception(f"Move {move} not found in Graph")
        for node,owner in nodes:
            blue_neighbours = 0
            kickouts = [(node,list(self.graph.edges(node,data=True)),owner)]
            for target,eattribs in self.graph.adj[node].items():
                if eattribs["color"]=="b":
                    if owner=="f":
                        revert_instructions.append((self.change_attrib,(target,"owner","f"),{}))
                        self.graph.nodes[target]["owner"] = self.graph.graph["onturn"]
                    elif owner!=self.graph.graph["onturn"]:
                        towner = self.graph.nodes[target]["owner"]
                        kickouts.append((target,list(self.graph.edges(target,data=True)),towner))
                    blue_neighbours+=1
            if owner==self.graph.graph["onturn"] and blue_neighbours==0:
                win = True
            for kickout,addedges,own in kickouts:
                revert_instructions.append((self.graph.add_edges_from,(addedges,),{}))
                self.graph.remove_node(kickout)
        revert_instructions.append((self.change_graph_attrib,("onturn",self.graph.graph["onturn"]),{}))
        revert_instructions.append((self.change_graph_attrib,("hash",self.graph.graph["hash"]),{}))
        self.revert_history.append(reversed(revert_instructions))
        self.graph.graph["onturn"] = "b" if self.graph.graph["onturn"]=="w" else "w"
        self.hashme()
        return win

    def draw_me(self,with_labels=False):
        pos = nx.spring_layout(self.graph, pos=self.random_pos)
        edges = self.graph.edges()
        colors = [self.graph[u][v]['color'] for u,v in edges]
        node_colors = []
        for node,nattribs in self.graph.nodes(data=True):
            if nattribs["owner"] == "f":
                node_colors.append('blue')
            elif nattribs["owner"] == "b": 
                node_colors.append('black')
            else:
                node_colors.append("red")
        nx.draw(self.graph,pos=pos, edge_color=colors, node_color=node_colors,with_labels=with_labels,font_color="white")
        plt.show()