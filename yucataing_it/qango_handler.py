import sys,os
import json
base_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(base_path)
sys.path.append(os.path.join(base_path,".."))
from ai_api import Ai_api

class Qango_handler():
    def __init__(self):
        self.ai = Ai_api({"qango6x6":[0,1,2,3],"qango7x7":[0,1,2,3],"qango7x7_plus":[0,1,2]})
        with open(os.path.join(base_path,"secrets.json"),"r") as f:
            self.secrets = json.load(f)

    def handle_get(self,uri,query):
        key = query.get('key', [None])[0]
        if key is None or key!=self.secrets["api_code"]:
            return "NOT FOUND"
        position = query.get('position', [None])[0]
        onturn = query.get('onturn', [None])[0]
        game_type = query.get('game_type', [None])[0]
        ruleset = query.get('ruleset', [None])[0]
        if position is None or onturn is None or game_type is None or ruleset is None:
            return [b"Invalid request"]
        position = list(position)
        ruleset = int(ruleset)
        move = self.ai.get_move(game_type,ruleset,onturn,position)
        return [str(move).encode()]
        
    def __call__(self,uri,query):
        self.handle_get(uri,query)