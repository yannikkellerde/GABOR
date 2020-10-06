import networkx as nx
from collections import defaultdict

class Board_game():
    winsquarenums:set
    position:list
    squares:int
    onturn:bool

    def __init__(self):
        self.onturn = "b"
    
    def to_graph(self):
        G = nx.Graph(onturn='b')
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