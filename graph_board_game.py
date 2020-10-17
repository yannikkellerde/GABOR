from graph_tool.all import *
import pickle
import math

class Board_game():
    winsquarenums:set
    position:list
    squares:int
    onturn:bool
    wp_map_rev:dict
    node_map_rev:dict

    def __init__(self):
        self.onturn = "b"
        self.node_map = dict()
        self.wp_map = dict()
        self.provenset_black = set()
        self.disprovenset_black = set()
        self.provenset_white = set()
        self.disprovenset_white = set()
    
    def inv_maps(self):
        self.wp_map_rev = {value:key for key,value in self.wp_map.items()}
        self.node_map_rev = {value:key for key,value in self.node_map.items()}

    def pos_from_graph(self):
        known_nods = [self.node_map[int(x)] for x in self.game.view.vertices() if self.game.owner_map[self.game.view.vp.o[x]] is None]
        pos = ["A"]*self.squares
        for key,value in self.wp_map.items():
            try:
                owner = self.game.owner_map[self.game.view.vp.o[self.game.view.vertex(key)]]
            except ValueError:
                continue
            for sq in value:
                if sq in known_nods:
                    pos[sq] = "f"
                else:
                    pos[sq] = owner
        return pos

    def load_sets(self,provenfile_black=None,disprovenfile_black=None,provenfile_white=None,disprovenfile_white=None):
        if provenfile_black is not None:
            with open(provenfile_black,"rb") as f:
                self.provenset_black = pickle.load(f)
        if disprovenfile_black is not None:
            with open(disprovenfile_black,"rb") as f:
                self.disprovenset_black = pickle.load(f)
        if provenfile_white is not None:
            with open(provenfile_white,"rb") as f:
                self.provenset_white = pickle.load(f)
        if disprovenfile_white is not None:
            with open(disprovenfile_white,"rb") as f:
                self.disprovenset_white = pickle.load(f)

    def check_move_val(self,moves,do_threat_search=True,priorize_sets=True):
        winmoves = self.game.win_threat_search(one_is_enough=False)
        if do_threat_search:
            self.game.view.gp["b"] = not self.game.view.gp["b"]
            defense_vertices,has_threat,_ = self.game.threat_search()
            self.game.view.gp["b"] = not self.game.view.gp["b"]
        results = []
        storage = self.game.extract_storage()
        for move in moves:
            val = "u"
            self.game.load_storage(storage)
            if do_threat_search and has_threat and move not in defense_vertices:
                if self.game.onturn=="b":
                    val = -3
                else:
                    val = 3
            else:
                self.game.make_move(move)
                self.game.hashme()
                if self.game.hash in self.provenset_white:
                    val = -2
                elif self.game.hash in self.provenset_black:
                    val = 2
                elif self.game.hash in self.disprovenset_white:
                    val = 1
                elif self.game.hash in self.disprovenset_black:
                    val = -1
                if val=="u" or not priorize_sets:
                    if self.game.view.num_vertices() == 0:
                        val = 0
                    else:
                        if move in winmoves:
                            if self.game.onturn=="b":
                                val = -4
                            else:
                                val = 4
                        else:
                            movs = len(self.game.win_threat_search(one_is_enough=True))>0
                            if movs:
                                if self.game.onturn=="b":
                                    val = 4
                                else:
                                    val = -4
            results.append(val)
        return results

    def make_move(self, move):
        self.position[move] = self.onturn
        self.onturn = "b" if self.onturn == "w" else "b"
        self.game.graph_from_board()      
        self.create_node_hash_map()

    def set_position(self,pos,onturn):
        self.position = pos
        self.onturn = onturn
        self.game.graph_from_board()

    def draw_me(self,pos=None):
        root = int(math.sqrt(self.squares))
        out_str = "#"*(root+2)
        out_str+="\n"
        pos = self.position if pos is None else pos
        for row in range(root):
            out_str+="#"
            for col in range(root):
                out_str += " " if pos[col+row*root]=="f" else pos[col+row*root]
            out_str+="#\n"
        out_str += "#"*(root+2)
        print(out_str)
        return out_str