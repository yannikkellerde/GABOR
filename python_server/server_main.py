import sys
sys.path.append("..")
sys.path.append(".")
from patterns_games import Tic_tac_toe, Qango6x6
import math
import json

from util import draw_board
import cgi
import threading
import webbrowser
from http.server import HTTPServer,SimpleHTTPRequestHandler
from functools import reduce
import os

FILE = "python_server/explore_wins.html"
PORT = 8080

def evaluate(game,hashval,proofconditions = [True,None]):
    posval = game.check_any_win()
    if posval is not None:
        return posval in proofconditions
    fullval = game.check_full()
    if fullval:
        return None in proofconditions
    if hashval in provenset_endgame:
        return True
    if hashval in disprovenset_endgame:
        return False
    return None

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
        real_pos = [sum(1<<i for i,a in enumerate(data["position"]) if a==pnum) for pnum in [1,2]]
        game.set_state(real_pos,data["onturn"])
        curhash = hash(game)
        draw_board(game.position,game.squares)
        print(game.aval_squares)
        curval = evaluate(game,curhash)
        movevals = {"current":curval}
        evalmap = {None:0,False:1,True:2}
        print(game.get_actions(),game.winhash)
        for move in game.get_actions():
            game.set_state(real_pos,data["onturn"])
            game.make_move(move)
            movevals[int(math.log(move,2))] = evalmap[evaluate(game,hash(game))]
        # add a property to the object, just to mess with data
        
        # send the message back
        self._set_headers()
        self.wfile.write(json.dumps(movevals).encode())


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

game = Tic_tac_toe(zobrist_file="../zobrist.pkl")
proof_path = os.path.join(sys.argv[2],"proof.txt")
disproof_path = os.path.join(sys.argv[2],"disproof.txt")
end_proof_path = os.path.join(sys.argv[2],"endproof.txt")
end_disproof_path = os.path.join(sys.argv[2],"enddisproof.txt")
endgame_depth = 0

with open(proof_path,"r") as f:
    provenset = set(map(int,f.read().split(",")[:-1]))
with open(disproof_path,"r") as f:
    disprovenset = set(map(int,f.read().split(",")[:-1]))
with open(end_proof_path,"r") as f:
    provenset_endgame = set(map(int,f.read().split(",")[:-1]))
with open(end_disproof_path,"r") as f:
    disprovenset_endgame = set(map(int,f.read().split(",")[:-1]))

print(len(provenset),len(disprovenset))

if __name__ == "__main__":
    my_folder = sys.argv[1]
    open_browser()
    start_server()
