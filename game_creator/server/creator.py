import os,sys
import json
from flask import render_template

base_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.join(base_path,"..","client")

class Game_creator_handler():
    def handle_get(self,gname):
        return render_template("game_creator.html",game_name=gname)
    def handle_post(self,game_name,data):
        if "game" in data:
            with open(os.path.join(root_path,"../../json_games",data["game"]["name"]+".json"),"w") as f:
                json.dump(data["game"],f)
            path = os.path.join(root_path,"../../rulesets",data["game"]["name"]+".json")
            if not os.path.isfile(path):
                with open(path,"w") as f:
                    json.dump({"default":[]},f)
            return json.dumps({"result":"save successfull"})
        elif "request" in data:
            if data["request"]=="config":
                json_path = os.path.join(base_path,"../../json_games",game_name+".json")
                if os.path.isfile(json_path):
                    with open(json_path,"r") as f:
                        return {"config":f.read()}
                else:
                    return {}
        return {"error":"invalid request"}


creator_handler = Game_creator_handler()