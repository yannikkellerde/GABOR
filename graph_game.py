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

    @property
    def hash(self):
        return self.graph.graph["hash"]

    def change_attrib(self,node,attrib,value):
        self.graph.nodes[node][attrib] = value

    def hashme(self):
        wl_hash(self.graph,edge_attr="color",node_attr="owner")

    def reset(self):
        self.graph = self.startgraph.copy()

    def revert_moves(self,amount):
        for _ in range(amount):
            if len(instructions)==0:
                self.hashme()
                return False
            instructions = self.revert_history.pop()
            for instruction in instructions:
                instruction()
        self.hashme()
        return True
    
    def get_actions(self):
        alreadymaps = {}
        for node,nattribs in self.graph.nodes(data=True):
            toadd = None
            blue_neighbours = 0
            for target,tattribs in self.graph.adj[node].items():
                if tattribs["color"] == "g":
                    if target in alreadymaps:
                        toadd = target
                else:
                    blue_neighbours += 1
            print(len(alreadymaps))
            if toadd is None:
                alreadymaps[node] = [blue_neighbours,[nattribs["label"]]]
            else:
                alreadymaps[toadd][1].append(nattribs["label"])
                alreadymaps[toadd][0] += blue_neighbours
        actions = list(OrderedSet([frozenset(x[1]) for x in sorted(alreadymaps.values(),key=lambda x:-len(x[1])*1000+x[0])]))
        return actions
    
    def make_move(self,move):
        revert_instructions = []
        win = False
        for node,nattribs in self.graph.nodes(data=True):
            if nattribs["label"] in move:
                nodes = {(node,nattribs["owner"])}
                labels = {nattribs["label"]}
                for target,tattribs in self.graph.adj[node].items():
                    if tattribs["color"]=="g":
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
            for target,tattribs in self.graph.adj[node].items():
                if tattribs["color"]=="b":
                    if owner=="f":
                        revert_instructions.append(lambda :self.change_attrib(target,"owner","f"))
                        self.graph.nodes[target]["owner"] = self.graph.graph["onturn"]
                    elif owner!=self.graph.graph["onturn"]:
                        revert_instructions.append(lambda :self.graph.add_edges_from(list(self.graph.edges(target))))
                        self.graph.remove_node(target)
                    blue_neighbours+=1
            if owner==self.graph.graph["onturn"] and blue_neighbours==0:
                win = True
            revert_instructions.append(lambda :self.graph.add_edges_from(list(self.graph.edges(node))))
            self.graph.remove_node(node)
        self.revert_history.append(reversed(revert_instructions))
        self.hashme()
        self.graph.graph["onturn"] = "b" if self.graph.graph["onturn"]=="w" else "w"
        return win

    def draw_me(self,with_labels=False):
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
        nx.draw(self.graph, edge_color=colors, node_color=node_colors,with_labels=with_labels)
        plt.show()