from solve_patterns_game import PN_search
from patterns_games import Tic_tac_toe,Qango6x6
from data_magic import save_sets
import os

def do_a_task(task):
    if not os.path.exists(os.path.dirname(task["solver_args"]["prooffile"])):
        os.makedirs(os.path.dirname(task["solver_args"]["prooffile"]))
    game = task["game_type"](**task["game_args"])
    solver = PN_search(game,**task["solver_args"])
    solver.pn_search()
    save_sets((solver.provenset,solver.prooffile),(solver.disprovenset,solver.disprooffile),
              (solver.endgame_provenset,solver.endgame_prooffile),(solver.endgame_disprovenset,solver.endgame_disprooffile))

tasks_q = [
    {
        "game_type":Qango6x6,
        "game_args":{
            "startpos":[[0,256],False],
            "zobrist_file":"zobrist.pkl"            
        },
        "solver_args":{
            "startdepth":1,
            "endgame_depth":0,
            "drawproves":False,
            "prooffile":"proofsets/qango6x6/proof.txt",
            "disprooffile":"proofsets/qango6x6/disproof.txt",
            "endgame_prooffile":"proofsets/qango6x6/endproof.txt",
            "endgame_disprooffile":"proofsets/qango6x6/enddisproof.txt"
        }
    }
]
tasks_tic = [
    {
        "game_type":Tic_tac_toe,
        "game_args":{
            "startpos":[[0,0],True],
            "zobrist_file":"zobrist.pkl"
        },
        "solver_args":{
            "startdepth":0,
            "endgame_depth":0,
            "drawproves":False,
            "prooffile":"proofsets/tic_tac_toe/proof.txt",
            "disprooffile":"proofsets/tic_tac_toe/disproof.txt",
            "endgame_prooffile":"proofsets/tic_tac_toe/endproof.txt",
            "endgame_disprooffile":"proofsets/tic_tac_toe/enddisproof.txt"
        }
    }
]

for task in tasks_tic:
    do_a_task(task)