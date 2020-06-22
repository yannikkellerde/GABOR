import json
import math
import sys

def replacements(root, parent_pos):
    if root["pn"] == math.inf:
        root["pn"] = "inf"
    if root["dn"] == math.inf:
        root["dn"] = "inf"
    if parent_pos is None:
        root["move"] = None
    else:
        root["move"] = int(math.log2(root["position"][not root["myturn"]]^parent_pos[not root["myturn"]]))
    for c in root["children"]:
        replacements(c, root["position"])
    del root["position"]

def dump_dict(game, root):
    with open(str(game)+"_js_readable.js","w") as file:
        file.write("tree = '")
        json.dump(root, file)
        file.write("'")


def save_the_noetigst(provenset, disprovenset, game):
    global addos
    def recurso(position, onturn):
        global addos
        game.set_state(position, onturn)
        addos += 1
        if addos % 10000 == 1:
            print(len(small_provenset), len(provenset))
        moves = game.get_actions()
        for move in moves:
            game.set_state(position, onturn)
            game.make_move(move)
            if game.check_win(move) or game.check_full():
                continue
            hashval = game.hashpos()
            if (hashval in provenset) and (not (hashval in small_provenset)):
                small_provenset.add(hashval)
                recurso(game.position, game.onturn)
                if onturn == 1:
                    return
    addos = 0
    game.reset()
    small_provenset = set()
    small_disprovenset = set()
    recurso(game.position, game.onturn)
    with open("small_disprovenset.txt","w") as file:
        for d in small_disprovenset:
            file.write(str(d)+",")
    with open("small_provenset.txt","w") as file:
        for p in small_provenset:
            file.write(str(p)+",")


def save_solution(node, file, game, parent_pos):
    if parent_pos is None:
        move = "null"
        game.reset()
    else:
        game.set_state(parent_pos, not node.myturn)
        move = game.extract_move(node.position)
        game.make_move(move)
        move = math.log2(move)
    file.write('{{"pn":{},"dn":{},"myturn":{},"move":{},"children":['.format(
        '"inf"' if node.pn == math.inf else node.pn,
        '"inf"' if node.dn == math.inf else node.dn,
        "true" if node.myturn else "false",
        move
    ))
    alr = False
    ppos = game.position[:]
    for c in node.children:
        if not node.myturn or c.pn == 0:
            if alr:
                file.write(",")
            save_solution(c, file, game, ppos)
            alr = True
    file.write("]}")

def save_sets(*sets_with_file):
    for ps,pf in sets_with_file:
        with open(pf,"w") as file:
            for d in ps:
                file.write(str(d)+",")

def save_tree_depth(node, file, game, parent_pos, depth, maxdepth):
    if parent_pos is None:
        move = "null"
        game.reset()
    else:
        game.set_state(parent_pos, not node.myturn)
        move = game.extract_move(node.position)
        game.make_move(move)
        move = math.log2(move)
    file.write('{{"pn":{},"dn":{},"myturn":{},"move":{},"children":['.format(
        '"inf"' if node.pn == math.inf else node.pn,
        '"inf"' if node.dn == math.inf else node.dn,
        "true" if node.myturn else "false",
        move
    ))
    alr = False
    ppos = game.position[:]
    if depth < maxdepth:
        for c in node.children:
            if alr:
                file.write(",")
            save_tree_depth(c, file, game, ppos, depth+1, maxdepth)
            alr = True
    file.write("]}")