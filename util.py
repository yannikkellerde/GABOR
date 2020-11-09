import math
import psutil
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt

def draw_pn_tree(root,depth=3):
    global count
    def add_nodes_recur(cur,depth):
        global count
        g.add_node(count,label=f"{cur[PN]}|{cur[DN]}")
        node_sizes.append(900 if depth>0 else 150)
        font_sizes[count] = 7 if depth>0 else 4
        my_c = count
        count += 1
        if depth<=0:
            return my_c
        for child in cur[CHILDREN]:
            c_num = add_nodes_recur(child,depth-1)
            g.add_edge(my_c,c_num)
        return my_c
    node_sizes = []
    font_sizes = {}
    plt.cla()
    # Node storage for memory efficency in lists
    PN = 0 # int
    DN = 1 # int
    HASH = 2 # int
    PARENTS = 3 # List of Nodes(which are lists)
    CHILDREN = 4 # List of tuples containing move made and Node (which is a lists)
    PROOFNODE = 5 # Bool, are we in a proof node or disproof node
    STORAGE = 6 # A tuple containing 1. an owner map, 2. a filter map, 3. onturn bool
    count = 0
    g = nx.DiGraph()
    add_nodes_recur(root,depth)
    plt.figure(figsize=(20,10)) 
    write_dot(g,'test.dot')
    pos = graphviz_layout(g, prog='dot')
    nx.draw(g, pos, with_labels=False, arrows=True, node_color="lightblue", node_size=node_sizes)
    node_labels = nx.get_node_attributes(g,'label')
    #nx.draw_networkx_labels(g, pos, labels = node_labels, font_size=font_sizes, font_color="white")
    for node, (x, y) in pos.items():
        plt.text(x, y, node_labels[node], fontsize=font_sizes[node], ha='center', va='center', color="black")
    plt.savefig('pn_tree.svg')
    plt.close()


def findsquares(squares):
    winsquarenums = set()
    perrow = int(math.sqrt(squares))
    for s in range(squares-perrow-1):
        if s % perrow != perrow-1:
            winsquarenums.add(frozenset({s,s+1,s+perrow,s+perrow+1}))
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
                winsquarenums.add(frozenset({s,s+perrow+1,s+2*(perrow+1),s+3*(perrow+1),s+4*(perrow+1)}))
        if perrow - (s // perrow) >= 5:
            winsquarenums.add(frozenset({s,s+perrow,s+2*perrow,s+3*perrow,s+4*perrow}))
            if (s % perrow) >= 4:
                winsquarenums.add(frozenset({s,s+perrow-1,s+2*(perrow-1),s+3*(perrow-1),s+4*(perrow-1)}))
    return winsquarenums

def resources_avaliable():
    memory = psutil.virtual_memory()
    if memory.percent > 97:
        return False
    return True

room_num = 0
def provide_room_num():
    global room_num
    room_num+=1
    if room_num > 1e7:
        room_num = 0
    return room_num