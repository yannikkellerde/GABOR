import sys
sys.path.append("..")
sys.path.append(".")
from graph_games import Tic_tac_toe, Qango6x6
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
PORT = 8080

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
        game.board_representation.set_position(real_pos,"b" if data["onturn"]==1 else "w")
        game.board_representation.draw_me()
        moves = game.get_actions()
        if moves is None:
            moves = []
        game.board_representation.create_node_hash_map()
        board_moves = [game.board_representation.convert_move(x) for x in moves]
        curval = None if game.hash not in game.board_representation.ttable else game.board_representation.ttable[game.hash]
        moves_with_eval = [("current",curval)]+[(game.board_representation.convert_move(x),game.board_representation.check_move_val(x)) for x in moves]
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
    """Start the server."""
    server_address = ("", PORT)
    server = HTTPServer(server_address, Post_handler)
    server.serve_forever()

game = Qango6x6()
with open("../alpha_beta.pkl","rb") as f:
    game.board_representation.ttable = pickle.load(f)
endgame_depth = 0

if __name__ == "__main__":
    my_folder = sys.argv[1]
    open_browser()
    start_server()
