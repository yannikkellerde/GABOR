import math
import psutil

def findsquares(squares):
    winsquarenums = set()
    perrow = int(math.sqrt(squares))
    for s in range(squares-perrow-1):
        if s % perrow != perrow-1:
            winsquarenums.add(frozenset({s,s+1,s+6,s+7}))
    return winsquarenums

def remove_useless_wsn(winsquarenums):
    discardos = set()
    for ws1 in winsquarenums:
        for ws2 in winsquarenums:
            if ws1!=ws2 and ws1.issubset(ws2):
                discardos.add(ws2)
    for d in discardos:
        winsquarenums.discard(d)
def findfivers(squares):
    winsquarenums = set()
    perrow = int(math.sqrt(squares))
    for s in range(squares):
        if perrow - (s % perrow) >= 5:
            winsquarenums.add(frozenset({s,s+1,s+2,s+3,s+4}))
            if perrow - (s // perrow) >= 5:
                winsquarenums.add(frozenset({s,s+7,s+14,s+21,s+28}))
        if perrow - (s // perrow) >= 5:
            winsquarenums.add(frozenset({s,s+6,s+12,s+18,s+24}))
            if (s % perrow) >= 4:
                winsquarenums.add(frozenset({s,s+5,s+10,s+15,s+20}))
    return winsquarenums

def buildupnodestruct(Node, moves, root, game, ttable):
    cur = root
    for move in moves:
        game.set_state(cur.position, cur.myturn)
        game.make_move(move)
        child = Node(game.onturn, game.position, cur, 1, 1)
        ttable[game.hashpos()] = child
        cur.children = [child]
        cur = child

def getwinhash(winpatterns, squares):
    winhash = {}
    pat_to_square = {w:set() for w in winpatterns}
    for s in range(squares):
        binsquare = 1<<s
        winhash[binsquare] = set()
        for w in winpatterns:
            if binsquare&w:
                pat_to_square[w].add(binsquare)
                winhash[binsquare].add(w)
    return winhash,pat_to_square

def draw_board(pos, squares):
    rowsquares = math.sqrt(squares)
    outstr=((int(rowsquares)+2)*"#")+"\n#"
    for i in range(squares):
        if pos[0]&(2**i):
            outstr+="O"
        elif pos[1]&(2**i):
            outstr+="X"
        else:
            outstr+=" "
        if i%rowsquares==rowsquares-1:
            outstr+="#\n#"
    outstr+=(int(rowsquares)+1)*"#"
    print(outstr)

def show_all_wins(game):
    for p in game.winpatterns:
        game.set_state([p,0],True)
        draw_board(game.position, 36)
        print("-----------------------------")

def test_game(game):
    while 1:
        draw_board(game.position, game.squares)
        print("choose one of the following actions")
        print(",".join(map(lambda x:str(int(math.log2(x))), game.get_actions())))
        #print(",".join(map(lambda x:str(int(math.log2(x))), game.get_actions_simple())))
        a = input()
        win = game.make_move(2**int(a))
        if win:
            print("You win")

def resources_avaliable():
    memory = psutil.virtual_memory()
    if memory.percent > 97:
        return False
    return True