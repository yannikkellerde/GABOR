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
        self.node_hash_map = dict()
        for vertex in self.graph_representation.graph.vertices():
            if self.graph_representation.graph.vp.o[vertex] == 0:
                self.node_hash_map[self.graph_representation.graph.vp.h[vertex]] = self.node_map[int(vertex)]
    
    def load_sets(self,provenfile,disprovenfile):
        with open(provenfile,"rb") as f:
            self.provenset = pickle.load(f)
        with open(disprovenfile,"rb") as f:
            self.disprovenset = pickle.load(f)

    def convert_move(self,move):
        return self.node_hash_map[move]

    def check_move_val(self,moves):
        self.graph_representation.graph.gp["b"] = not self.graph_representation.graph.gp["b"]
        defense_vertices,has_threat,_ = self.graph_representation.threat_search()
        self.graph_representation.graph.gp["b"] = not self.graph_representation.graph.gp["b"]
        if has_threat:
            defense_hashes = self.graph_representation.graph.vp.h.get_array()[list(defense_vertices)]
        results = []
        for move in moves:
            if has_threat and move not in defense_hashes:
                if self.graph_representation.onturn=="b":
                    val = 2
                else:
                    val = 3
            else:
                orig = Graph(self.graph_representation.graph)
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
                                    val = 5
                                else:
                                    val = 4
                            else:
                                if res:
                                    val = 4
                                else:
                                    val = 5
                self.graph_representation.graph = orig
            results.append(val)
        return results

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