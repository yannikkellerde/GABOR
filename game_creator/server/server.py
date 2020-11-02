import os,sys
import json
from urllib.parse import parse_qs

base_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.join(base_path,"..","client")

def path_is_parent(parent_path, child_path):
    # Smooth out relative path names, note: if you are concerned about symbolic links, you should use os.path.realpath too
    parent_path = os.path.abspath(parent_path)
    child_path = os.path.abspath(child_path)

    # Compare the common path of the parent and child path with the common path of just the parent path. Using the commonpath method on just the parent path will regularise the path name in the same way as the comparison that deals with both paths, removing any trailing path separator
    return os.path.commonpath([parent_path]) == os.path.commonpath([parent_path, child_path])

class Game_creator_handler():
    def __init__(self):
        self.ending_to_content_type = {
            "/":"text/html",
            "html": "text/html",
            "css": "text/css",
            "png": "image/png",
            "jpg": "image/jpeg",
            "js":"text/javascript",
            "jpeg": "image/jpeg",
            "json": "application/json"
        }
    def handle_get(self,uri,q):
        if uri=="/":
            uri="game_creator.html"
        else:
            uri = uri[1:]
        real_uri = os.path.join(root_path, uri)
        print(root_path,os.path.join(root_path, uri[1:]),uri,real_uri,path_is_parent(root_path,real_uri))
        if not path_is_parent(root_path,real_uri):
            return "NOT FOUND"
        try:
            with open(real_uri,"r") as f:
                my_content = f.read().encode()
        except FileNotFoundError:
            return "NOT FOUND"
        except UnicodeDecodeError as e:
            with open(real_uri,"rb") as f:
                my_content = f.read()
        return [my_content]
    def handle_post(self,data):
        print("RECEIVED POST REQUEST")
        print(data)
        if "game" in data:
            with open(os.path.join(root_path,"../../json_games",data["game"]["name"]+".json"),"w") as f:
                json.dump(data["game"],f)
        return [json.dumps({"result":"save successfull"}).encode()]

def application(environ, start_response):
    global handler
    try:  # This is disgusting!
        handler
    except:
        print("Creating the handler")
        handler = Game_creator_handler()
    uri = environ["REQUEST_URI"]
    if environ["REQUEST_METHOD"] == "GET":
        d = parse_qs(environ['QUERY_STRING'])
        out = handler.handle_get(uri,d)
    elif environ["REQUEST_METHOD"] == "POST":
        post_input = json.loads(environ['wsgi.input'].readline().decode())
        out = handler.handle_post(post_input)
    if out == "NOT FOUND":
        start_response('404 NOT FOUND', [('Content-Type',"text/html")])
        return [b"404 NOT FOUND"]
    if uri.split(".")[-1] in handler.ending_to_content_type:
        ct = handler.ending_to_content_type[uri.split(".")[-1]]
    else:
        ct = "text/plain"
    start_response('200 OK', [('Content-Type',ct)])
    return out