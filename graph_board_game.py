from graph_tool.all import *
import pickle
import math

class Board_game():
    winsquarenums:set
    position:list
    squares:int
    onturn:bool

    def __init__(self):
        self.onturn = "b"
        self.node_map = dict()
        self.node_hash_map = dict()
        self.provenset = set()
        self.disprovenset = set()

    def create_node_hash_map(self):
        for vertex in self.graph_representation.graph.vertices():
            if self.graph_representation.graph.vp.o[vertex] == 0:
                self.node_hash_map[self.graph_representation.graph.vp.h[vertex]] = self.node_map[vertex]
    
    def load_sets(self,provenfile,disprovenfile):
        with open(provenfile,"rb") as f:
            self.provenset = pickle.load(f)
        with open(disprovenfile,"rb") as f:
            self.disprovenset = pickle.load(f)

    def convert_move(self,move):
        return self.node_hash_map[move]

    def check_move_val(self, move):
        orig = Graph(self.graph_representation.graph)
        if move is not None:
            self.graph_representation.make_move(move)
        if self.graph_representation.hash in self.provenset:
            val = 1
        elif self.graph_representation.hash in self.disprovenset:
            val = -1
        else:
            if self.graph_representation.graph.num_vertices() == 0:
                val = 0
            else:
                orig_move = Graph(self.graph_representation.graph)
                res = self.graph_representation.forced_move_search()
                self.graph_representation.graph = orig_move
                if res is None:
                    val = "u"
                else:
                    if self.graph_representation.onturn=="b":
                        if res:
                            val = 1
                        else:
                            val = 2
                    else:
                        if res:
                            val = 2
                        else:
                            val = 1
        self.graph_representation.graph = orig
        return val

    def make_move(self, move):
        self.position[move] = self.onturn
        self.onturn = "b" if self.onturn == "w" else "b"
        self.graph_representation.graph_from_board()      
        self.create_node_hash_map()

    def set_position(self,pos,onturn):
        self.position = pos
        self.onturn = onturn
        self.graph_representation.graph_from_board()

    def draw_me(self):
        root = int(math.sqrt(self.squares))
        out_str = "#"*(root+2)
        out_str+="\n"
        for row in range(root):
            out_str+="#"
            for col in range(root):
                out_str += " " if self.position[col+row*root]=="f" else self.position[col+row*root]
            out_str+="#\n"
        out_str += "#"*(root+2)
        print(out_str)