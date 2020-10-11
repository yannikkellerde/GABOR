from graph_tool.all import *

def split_into_subgraphs(G:Graph):
    comp,hist = label_components(G,directed=False)
    if len(hist)==1:
        return [G]
    sub_graphs = []
    for i in range(len(hist)):
        u = GraphView(g, vfilt=comp.a == i)
        sub_graphs.append(Graph(u, prune=True))
    return sub_graphs

if __name__ == "__main__":
    g = Graph(directed=False)
    verts = list(g.add_vertex(10))
    for i in range(9):
        if i!=5:
            g.add_edge(verts[i],verts[i+1])
    subg = split_into_subgraphs(g)
    for i,sg in enumerate(subg):
        graph_draw(sg, vertex_text=sg.vertex_index, output=f"subg{i}.pdf")
