import networkx as nx
from graph_game import Graph_game
from collections import defaultdict

class Board_game():
    winsquarenums:set
    position:list
    squares:int
    onturn:bool
    graph_representation:Graph_game

    def __init__(self):
        self.onturn = "b"
        self.node_map = dict()
        self.node_hash_map = dict()
        self.ttable = dict()

    def create_node_hash_map(self):
        self.node_hash_map = [set() for _ in range(self.squares)]
        for key,value in dict(self.graph_representation.graph.nodes(data=True)).items():
            self.node_hash_map[self.node_map[key]].add(value["label"])
        self.node_hash_map = {frozenset(x):x for x in self.node_hash_map}
    
    def convert_move(self,move):
        return self.node_hash_map[move]

    def check_move_val(self, move):
        self.graph_representation.make_move(move)
        if self.graph_representation.hash in self.ttable:
            val = self.ttable[self.graph_representation.hash]
        else:
            val = None
        self.graph_representation.revert_moves(1)
        return val

    def make_move(self, move):
        self.position[move] = onturn
        self.onturn = "b" if onturn == "w" else "b"
        self.graph_representation.set_graph(self.to_graph)
        self.create_node_hash_map()

    def to_graph(self):
        G = nx.Graph(onturn=self.onturn)
        nodecounter = 0
        samesquares = defaultdict(set)
        for wsn in self.winsquarenums:
            created = []
            wp_type = "f"
            for ws in wsn:
                if self.position[ws] != "f":
                    if wp_type == "f":
                        wp_type = self.position[ws]
                    else:
                        if self.position[ws]!=wp_type:
                            wp_type = "out"
            if wp_type == "out":
                continue
            for ws in wsn:
                if self.position[ws]!="f":
                    continue
                G.add_node(nodecounter,owner=wp_type)
                self.node_map[nodecounter]=ws
                created.append(nodecounter)
                if ws in samesquares:
                    for other in samesquares[ws]:
                        G.add_edge(nodecounter, other, color='g')
                samesquares[ws].add(nodecounter)
                nodecounter+=1
            for c in range(len(created)):
                for j in range(c+1,len(created)):
                    G.add_edge(created[c],created[j],color='b')
        return G