import os,sys
import json
from urllib.parse import parse_qs
from flask import render_template

base_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.join(base_path,"..","client")

class Game_creator_handler():
    def handle_get(self):
        return render_template("game_creator.html")
    def handle_post(self,data):
        print("RECEIVED POST REQUEST")
        print(data)
        if "game" in data:
            with open(os.path.join(root_path,"../../json_games",data["game"]["name"]+".json"),"w") as f:
                json.dump(data["game"],f)
            path = os.path.join(root_path,"../../rulesets",data["game"]["name"]+".json")
            if not os.path.isfile(path):
                with open(path,"w") as f:
                    json.dump({"default":[]},f)
        return json.dumps({"result":"save successfull"})

creator_handler = Game_creator_handler()