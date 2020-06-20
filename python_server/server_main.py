from flask import session
from flask_socketio import emit
import sys
sys.path.append("..")
sys.path.append(".")
from qango6x6 import Quango6x6
import math
import json

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
    if hashval in provenset:
        return True
    if hashval in disprovenset:
        return False
    return None

class Post_handler(SimpleHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        # read the message and convert it into a python dictionary
        length = int(self.headers['Content-Length'])
        data_str = self.rfile.read(length)
        data = json.loads(data_str)
        real_pos = [sum(1<<i for i,a in enumerate(data["position"]) if a==pnum) for pnum in [1,2]]
        game.set_state(real_pos,data["onturn"])
        curhash = game.hashpos()
        print("###########\n",real_pos,"\n",curhash,'\n############')
        curval = evaluate(game,curhash)
        movevals = {"current":curval}
        evalmap = {None:0,False:1,True:2}
        for move in game.get_actions_simple():
            game.set_state(real_pos,data["onturn"])
            game.make_move(move)
            movevals[int(math.log(move,2))] = evalmap[evaluate(game,game.hashpos())]
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

game = Quango6x6()
with open(sys.argv[1],"r") as f:
    provenset = set(map(int,f.read().split(",")[:-1]))
with open(sys.argv[2],"r") as f:
    disprovenset = set(map(int,f.read().split(",")[:-1]))

print(len(provenset),len(disprovenset))

if __name__ == "__main__":
    open_browser()
    start_server()
