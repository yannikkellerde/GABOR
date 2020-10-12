import sys
sys.path.append("..")
sys.path.append(".")
from graph_tools_games import Tic_tac_toe, Qango6x6
import math
import pickle
import json

import cgi
import threading
import webbrowser
from http.server import HTTPServer,SimpleHTTPRequestHandler
from functools import reduce
import os

FILE = "python_server/explore_wins.html"
PORT = 8081

class Post_handler(SimpleHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        if self.path.endswith("explore_wins.html"):
            self.send_response(200)

            # Setting the header
            self.send_header("Content-type", "text/html")

            # Whenever using 'send_header', you also have to call 'end_headers'
            self.end_headers()
            with open("explore_wins.html","r") as f:
                my_content = f.read()
            with open(os.path.join(my_folder,"board.html"),"r") as f:
                my_board = f.read()
            with open(os.path.join(my_folder,"game.js"),"r") as f:
                my_js = f.read()
            my_content = (my_content.split("<!--Insert board here-->")[0] +
                        my_board +
                        my_content.split("<!--Insert board here-->")[1]
            )
            my_content = (my_content.split("<!--Insert link to stylesheet here-->")[0] +
                         '<link rel="stylesheet" href="/'+os.path.join(my_folder,"board.css")+'">' +
                          my_content.split("<!--Insert link to stylesheet here-->")[1])
            my_content = (my_content.split("<!--Insert path to gamescript here-->")[0] +
                        "<script>"+my_js+"</script>" +
                        my_content.split("<!--Insert path to gamescript here-->")[1])
            self.wfile.write(my_content.encode())
        else:
            super().do_GET()

    def do_POST(self):
        # read the message and convert it into a python dictionary
        length = int(self.headers['Content-Length'])
        data_str = self.rfile.read(length)
        data = json.loads(data_str)
        real_pos = [("f" if x==0 else ("b" if x==2 else "w")) for x in data["position"]]
        game.board.set_position(real_pos,"b" if data["onturn"]==1 else "w")
        game.board.draw_me()
        moves = game.get_actions()
        if moves is None:
            moves = []
        game.board.create_node_hash_map()
        board_moves = [game.board.convert_move(x) for x in moves]
        game.draw_me()
        evals = game.board.check_move_val(moves)
        moves_with_eval = list(zip(board_moves, evals))
        # send the message back
        self._set_headers()
        self.wfile.write(json.dumps({"moves":moves_with_eval}).encode())

def self_contained_evaluator(real_pos,onturn):
    p = list( "ffffff"
                  "ffffff"
                  "ffffff"
                  "ffffff"
                  "ffwbff"
                  "ffffff")
    if real_pos!=p:
        return
    ingame = Qango6x6()
    ingame.board.load_sets("../proofsets/burgregelp.pkl","../proofsets/burgregeld.pkl")
    print(real_pos,onturn)
    ingame.board.set_position(real_pos,onturn)
    ingame.graph.gp["b"] = not ingame.graph.gp["b"]
    defense_vertices,has_threat,movelines = ingame.threat_search()
    for line in movelines:
        print([d if type(d)==str else (d,(ingame.board.node_map[d]%6,ingame.board.node_map[d]//6)) for d in line[1:]])
    print("Self contained",has_threat,len(defense_vertices),ingame.onturn)
    ingame.graph.gp["b"] = not ingame.graph.gp["b"]

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
    if "qango" in my_folder:
        game = Qango6x6()
    else:
        game = Tic_tac_toe()
    game.board.load_sets("../proofsets/burgregelp.pkl","../proofsets/burgregeld.pkl")
    endgame_depth = 0
    open_browser()
    start_server()
