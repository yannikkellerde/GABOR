import os,sys
solver_root = "."
solver_analyze_path = os.path.join(solver_root,"analyzer")
solver_creator_path = os.path.join(solver_root,"game_creator/server")
go_path = ""
sys.path.append(solver_analyze_path)
sys.path.append(solver_creator_path)
sys.path.append(solver_root)
sys.path.append(go_path)
from analyzer import analyze_handler
from solver_main import solver_handler
from creator import creator_handler
import uuid
import json
import jinja2
from flask import Flask, request, send_from_directory, session, render_template, redirect, send_file
from flask_socketio import SocketIO, emit
app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SESSION_COOKIE_SAMESITE'] = "Strict"
socketio = SocketIO(app)
room_num = 0

my_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader([os.path.join(solver_analyze_path,"templates"), 
                                 os.path.join(solver_root,"game_creator","client","templates"),
                                 os.path.join(solver_root,"static","templates")]),
    ])
app.jinja_loader = my_loader

def create_id():
    if "uid" not in session:
        session["uid"] = uuid.uuid4()

@app.route('/favicon.ico')
def getfavicon():
    return send_file(os.path.join(solver_root,"images/schiff.ico"), mimetype='image/ico')
@app.route('/')
def main_page():
    create_id()
    return redirect("/solver", code=302)
@app.route('/go')
def go_opening_explorer():
    create_id()
    pass
@app.route('/solver',methods=['GET', 'POST'])
def solver_select_page():
    create_id()
    if request.method == 'GET':
        return solver_handler.do_GET()
    else:
        return solver_handler.do_POST(request.json)
@app.route('/solver/analyze/<path:game>',methods=['GET', 'POST'])
def solver_analyzer(game):
    create_id()
    if request.method == 'POST':
        res = analyze_handler.do_POST(request.json,session["uid"])
        return res
    else:
        return analyze_handler.do_GET(game,session["uid"])
@app.route('/solver/creator/<path:game>',methods=['GET', 'POST'])
def solver_creator(game):
    create_id()
    if request.method == 'POST':
        return creator_handler.handle_post(game,request.json)
    else:
        return creator_handler.handle_get(game)

# SocketIO stuff
@socketio.on('connect')
def connect():
    create_id()
    print("User connected",request.sid,session["uid"])

@socketio.on('disconnect')
def disconnect():
    if request.sid in analyze_handler.sid_to_thread:
        analyze_handler.sid_to_thread[request.sid].do_run = False
    print('Client disconnected',request.sid,session["uid"])

@socketio.on('start_search')
def start_search(data):
    print("Got start search request")
    analyze_handler.start_search(data,request.sid,session["uid"],socketio)


# Static stuff
@app.route('/static_analyzer/<path:path>')
def serve_game_json(path):
    return send_from_directory(os.path.join(solver_root,"analyzer"),path)
@app.route('/static_creator/<path:path>')
def serve_creator_static(path):
    return send_from_directory(os.path.join(solver_root,'game_creator/client/'),path)
@app.route('/static_solver/<path:path>')
def serve_static(path):
    return send_from_directory(os.path.join(solver_root,'static/'),path)
