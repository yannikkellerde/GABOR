from solve_patterns_game import PN_search
from patterns_games import Tic_tac_toe
from data_magic import save_sets

def do_a_task(task):
    game = Tic_tac_toe(**task["game_args"])
    solver = PN_search(game,**task["solver_args"])
    solver.pn_search()
    save_sets((solver.provenset,solver.prooffile),(solver.disprovenset,solver.disprooffile),
              (solver.endgame_provenset,solver.endgame_prooffile),(solver.endgame_disprovenset,solver.endgame_disprooffile))

tasks = [
    {
        "game_args":{
            "startpos":[[0,0],True],
            "zobrist_file":"zobrist.pkl"            
        },
        "solver_args":{
            "endgame_depth":0,
            "drawproves":False,
            "prooffile":"proofsets/tic_tac_toe/proof.txt",
            "disprooffile":"proofsets/tic_tac_toe/disproof.txt",
            "endgame_prooffile":"proofsets/tic_tac_toe/endproof.txt",
            "endgame_disprooffile":"proofsets/tic_tac_toe/enddisproof.txt"
        }
    }
]

for task in tasks:
    do_a_task(task)