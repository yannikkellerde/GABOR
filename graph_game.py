import math
from tqdm import tqdm,trange
from copy import copy,deepcopy
from functools import reduce
import time
import numpy as np
import pickle
import networkx as nx

from graph_hashing import wl_hash

class Graph_game():
    graph:nx.Graph
    startgraph:nx.Graph
    def __init__(self):
        pass
    def reset(self):
        self.graph = startgraph.copy()
    