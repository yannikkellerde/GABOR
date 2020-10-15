from graph_tools_games import Tic_tac_toe,Qango6x6,Qango7x7,Qango7x7_plus
from graph_tools_game import Graph_game
import math
import os
import numpy as np
import random
game_map = {"tic_tac_toe":Tic_tac_toe,"qango6x6":Qango6x6,"qango7x7":Qango7x7,"qango7x7_plus":Qango7x7_plus}
basepath = os.path.abspath(os.path.dirname(__file__))

class Ai_api():
    def __init__(self,games_with_rulsets):
        self.games = {}
        self.value_prio = {"w":[2,4,-1,0,"u",1,5,3],
                           "b":[3,5,1,0,"u",-1,2,4]}
        for game,rulesets in games_with_rulsets.items():
            rulemap = {}
            self.games[game] = rulemap
            for rule in rulesets:
                g = game_map[game]()
                g.board.load_sets(os.path.join(basepath,f"proofsets/{game}_{rule}p.pkl"),os.path.join(basepath,f"proofsets/{game}_{rule}d.pkl"))
                rulemap[rule] = g
    
    def get_move(self,game,ruleset,color,position):
        if game not in self.games or ruleset not in self.games[game]:
            raise ValueError("Unknown game {}/ ruleset {}".format(game,ruleset))
        g:Graph_game = self.games[game][ruleset]
        g.board.onturn = color
        g.board.position = position
        g.graph_from_board()
        depth = len(list(filter(lambda x:x!="f",position)))
        if depth==0:
            blocked,block_depths,threatblock = g.board.get_burgregel_blocked(ruleset)
        moves = g.get_actions(filter_superseeded=(depth!=0 or (depth not in block_depths)),none_for_win=False)
        if depth==0 and depth in block_depths:
            moves = [m for m in moves if m not in blocked]
        board_moves = [g.board.node_map[x] for x in moves]
        evals = g.board.check_move_val(moves,priorize_sets=False,do_threat_search=False)
        moves_with_eval = list(zip(board_moves,evals))
        best = math.inf
        best_move = []
        for move,ev in moves_with_eval:
            val = self.value_prio[color].index(ev)
            if val<best:
                best=val
                best_move = [move]
            elif val==best:
                best_move.append(move)
        best_move = best_move[:3]
        probs = np.array([0.7,0.2,0.1])
        probs = probs[:len(best_move)]
        probs = probs/np.sum(probs)
        res_move = int(np.random.choice(best_move,p=probs))
        return res_move