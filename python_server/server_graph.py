import sys
sys.path.append("..")
sys.path.append(".")
from graph_tools_games import Tic_tac_toe, Qango6x6, Qango7x7, Qango7x7_plus, Json_game
import math
import pickle
import json

import cgi
import threading
import webbrowser
from http.server import HTTPServer,SimpleHTTPRequestHandler
from functools import reduce
import os

base_path = os.path.abspath(os.path.dirname(__file__))

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
        if "request" in data:
            self._set_headers()
            self.wfile.write(json.dumps(game.config).encode())
        else:
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
            self._set_headers()
            self.wfile.write(json.dumps({"moves":moves_with_eval}).encode())

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
    game_name = my_folder
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
        game_name = sys.argv[2]
        start_arg = 3
    else:
        raise ValueError(f"Game not found {my_folder}")
    try:
        if len(sys.argv)>start_arg:
            game.board.load_sets(provenfile_black=f"../proofsets/b_{game_name}_{sys.argv[start_arg]}p.pkl",
                                 disprovenfile_black=f"../proofsets/b_{game_name}_{sys.argv[start_arg]}d.pkl")
        else:
            game.board.load_sets(provenfile_black=f"../proofsets/full_game/b_{game_name}_p.pkl",
                                 disprovenfile_black=f"../proofsets/full_game/b_{game_name}_d.pkl")
    except FileNotFoundError as e:
        print(e)
    try:
        if len(sys.argv)>start_arg:
            game.board.load_sets(provenfile_white=f"../proofsets/w_{game_name}_{sys.argv[start_arg]}p.pkl",
                                 disprovenfile_white=f"../proofsets/w_{game_name}_{sys.argv[start_arg]}d.pkl")
        else:
            game.board.load_sets(provenfile_white=f"../proofsets/full_game/w_{game_name}_p.pkl",
                                 disprovenfile_white=f"../proofsets/full_game/w_{game_name}_d.pkl")
    except FileNotFoundError as e:
        print(e)
    endgame_depth = 0
    open_browser()
    start_server()
