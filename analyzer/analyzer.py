import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(os.path.dirname(__file__))
print(sys.path)
from graph_tools_games import Tic_tac_toe, Qango6x6, Qango7x7, Qango7x7_plus, Json_game
import math
import pickle
import json
from collections import defaultdict
from flask import render_template

from functools import reduce
import os

base_path = os.path.abspath(os.path.dirname(__file__))

FILE = "python_server/explore_wins.html"
PORT = 8081

class Solver_analyze():
    def __init__(self):
        self.session_to_game = {}
        self.game_name_to_sessions = defaultdict(set)
        self.session_to_proofsets = {}
        self.proofsets_with_sessions = defaultdict(set)
        self.game_name_to_game = {}

    def get_proofsets()

    def get_game(self,game_name,uid):
        if not (uid in self.session_to_game and game_name_to_game[game_name] == self.session_to_game[uid]):
            if game_name not in self.game_name_to_game:
                if "qango6x6"==game_name:
                    game = Qango6x6()
                elif "qango7x7"==my_folder:
                    game = Qango7x7()
                elif "tic_tac_toe"==my_folder:
                    game = Tic_tac_toe()
                elif my_folder == "qango7x7_plus":
                    game = Qango7x7_plus()
                elif my_folder == "json":
                    game = Json_game(os.path.join(base_path,"../json_games",sys.argv[2]+".json"))
                self.game_name_to_game[game_name] = game
            self.session_to_game[uid] = self.game_name_to_game[game_name]
                self.game_name_to_sessions[game_name].add(uid)
        return self.session_to_game[uid]

    def do_GET(self,game_name):
        with open(os.path.join(base_path,game_name,"board.html"),"r") as f:
            my_board = f.read()
        return render_template(os.path.join("explore_wins.html"),board = my_board, stylesheet=os.path.join("/static_analyzer",game_name,"board.css"),
                               game_js_path=os.path.join("/static_analyzer",game_name,"game.js"))

    def create_proofset(self,new):
        path = os.path.join(base_path,"..","proofsets",new)
        if not os.path.exists(path):
            os.mkdir(path)
            for setname in game.board.psets:
                with open(os.path.join(path,setname+".pkl"), 'wb') as f:
                    pickle.dump(set(),f)

    def do_POST(self,data,uid):
        # read the message and convert it into a python dictionary
        out = json.dumps({"error":"NOT FOUND"})
        if "request" in data:
            if data["request"] == "config":
                out = json.dumps(game.config)
            if data["request"] == "rulesets":
                out = json.dumps(game.board.rulesets)
            if data["request"] == "aval_proofsets":
                proofsets = os.listdir(os.path.join(base_path,"..","proofsets"))
                out = json.dumps({"proofsets":proofsets,"default":game.name})
        elif "new_proofset" in data:
            self.create_proofset(data["new_proofset"])
            proofsets = os.listdir(os.path.join(base_path,"..","proofsets"))
            game.board.load_set_folder(os.path.join(base_path,"../proofsets",data["new_proofset"]))
            out = json.dumps({"proofsets":proofsets,"default":data["new_proofset"],"changed_to":data["new_proofset"]})
        elif "set_proofset" in data:
            game.board.load_set_folder(os.path.join(base_path,"../proofsets",data["set_proofset"]))
            out = json.dumps({"changed_to":data["set_proofset"]})
        elif "position" in data:
            real_pos = [("f" if x==0 else ("b" if x==2 else "w")) for x in data["position"]]
            print(real_pos,game.board.position)
            game.board.set_position(real_pos,"b" if data["onturn"]==1 else "w")
            game.board.draw_me()
            depth = len(list(filter(lambda x:x!="f",real_pos)))
            moves = game.get_actions(filter_superseeded=False,none_for_win=False)
            board_moves = [game.board.node_map[x] for x in moves]
            game.draw_me()
            evals = game.board.check_move_val(moves)
            moves_with_eval = list(zip(board_moves, evals))
            # send the message back
            out = json.dumps({"moves":moves_with_eval})
        elif "new_rule" in data:
            game.board.rulesets[data["new_rule"]] = data["blocked"]
            with open(os.path.join(base_path,"../rulesets",game.name+".json"),"w") as f:
                json.dump(game.board.rulesets,f)
            out = json.dumps(game.board.rulesets)
        elif "del_rule" in data:
            if (len(game.board.rulesets)>1):
                del game.board.rulesets[data["del_rule"]]
                with open(os.path.join(base_path,"../rulesets",game.name+".json"),"w") as f:
                    json.dump(game.board.rulesets,f)
            out = json.dumps(game.board.rulesets)
        return out

def open_browser():
    """Start a browser after waiting for half a second."""
    def _open_browser():
        webbrowser.open('http://localhost:%s/%s' % (PORT, FILE))
    thread = threading.Timer(0.5, _open_browser)
    thread.start()

def start_server():
    global PORT
    """Start the server."""
    while 1:
        server_address = ("", PORT)
        try:
            server = HTTPServer(server_address, Post_handler)
            break
        except OSError as e:
            PORT+=1
    server.serve_forever()

if __name__ == "__main__":
    my_folder = sys.argv[1]
    start_arg = 2
    if "qango6x6"==my_folder:
        game = Qango6x6()
    elif "qango7x7"==my_folder:
        game = Qango7x7()
    elif "tic_tac_toe"==my_folder:
        game = Tic_tac_toe()
    elif my_folder == "qango7x7_plus":
        game = Qango7x7_plus()
    elif my_folder == "json":
        game = Json_game(os.path.join(base_path,"../json_games",sys.argv[2]+".json"))
        start_arg = 3
    else:
        raise ValueError(f"Game not found {my_folder}")
    game.board.load_set_folder(os.path.join(base_path,"..","proofsets",game.name))
    endgame_depth = 0
    open_browser()
    start_server()
