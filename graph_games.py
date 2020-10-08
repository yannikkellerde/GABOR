from graph_game import Graph_game
from board_representation import Board_game
from util import findfivers, findsquares, remove_useless_wsn
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

def wsn_to_graph(wsns):
    """Transform winsquarenums to a startposition graph."""
    G = nx.Graph(onturn='b')
    nodecounter = 0
    samesquares = defaultdict(set)
    for wsn in wsns:
        created = []
        for ws in wsn:
            G.add_node(nodecounter,owner="f")
            created.append(nodecounter)
            if ws in samesquares:
                for other in samesquares[ws]:
                    G.add_edge(nodecounter, other, color='g')
            samesquares[ws].add(nodecounter)
            nodecounter+=1
        for c in range(len(created)):
            for j in range(c,len(created)):
                G.add_edge(created[c],created[j],color='b')
    return G

class Qango6x6(Graph_game):
    def __init__(self):
        self.board_representation = Qango6x6_board()
        self.board_representation.graph_representation = self
        self.graph = self.board_representation.to_graph()
        super().__init__()

class Qango6x6_board(Board_game):
    def __init__(self):
        self.squares = 36
        self.position = ["f" for _ in range(self.squares)]
        self.winsquarenums = {
            frozenset({0,1,6}),frozenset({4,5,11}),frozenset({24,30,31}),frozenset({29,34,35}),
            frozenset({2,7,12}),frozenset({3,10,17}),frozenset({18,25,32}),frozenset({23,28,33}),
            frozenset({8,13,14}),frozenset({9,15,16}),frozenset({19,20,26}),frozenset({21,22,27})
        }
        self.winsquarenums.update(findsquares(self.squares))
        self.winsquarenums.update(findfivers(self.squares))
        remove_useless_wsn(self.winsquarenums)
        super().__init__()

class Tic_tac_toe(Graph_game):
    def __init__(self):
        self.board_representation = Tic_tac_toe_board()
        self.board_representation.graph_representation = self
        self.graph = self.board_representation.to_graph()
        super().__init__()

class Tic_tac_toe_board(Board_game):
    def __init__(self):
        self.squares = 9
        self.position = ["f" for _ in range(self.squares)]
        self.winsquarenums = {frozenset({0,1,2}),frozenset({3,4,5}),frozenset({6,7,8}),
                              frozenset({0,3,6}),frozenset({1,4,7}),frozenset({2,5,8}),
                              frozenset({0,4,8}),frozenset({2,4,6})}
        super().__init__()

if __name__ == "__main__":
    q = Tic_tac_toe()
    edges = q.graph.edges()
    colors = ["r" if q.graph[u][v]['color']=="g" else "b" for u,v in edges]
    #plt.figure(num=None, figsize=(80, 80), dpi=80, facecolor='w', edgecolor='k')
    nx.draw(q.graph, edge_color=colors)
    plt.savefig("test.svg")
    plt.show()