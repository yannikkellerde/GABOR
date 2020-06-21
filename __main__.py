from game_solver import PN_DAG, reconstruct_vicory
from tic_tac_toe import Tic_tac_toe
from qango6x6 import Qango6x6
from data_magic import dump_dict, replacements, save_solution, save_tree_depth, save_sets, save_the_noetigst
import sys
import gc
import time

def do_a_task(task):
    game = Qango6x6(task[:2])
    solver = PN_DAG(game,drawproves=task[2],prooffile=task[3],disprooffile=task[4])
    solver.loadsets()
    while 1:
        res = solver.pn_search()
        save_sets(solver.provenset, solver.disprovenset,prooffile=task[3],disprooffile=task[4])
        print("Size transition table: {}, size provenset: {}, size disprovenset: {}".format(
            sys.getsizeof(solver.ttable),
            sys.getsizeof(solver.provenset),
            sys.getsizeof(solver.disprovenset)
        ))
        if res:
            print("game solved")
            save_the_noetigst(solver.provenset, solver.disprovenset, game)
            break
        else:
            print("No resouces left, game not solved yet.")
            print("Making the memory test now")
            del solver.root
            del solver.ttable
            solver.ttable = {}
            solver.proofadds = [0,0]
            print("Deleted big objects, collecting garbage now")
            gc.collect()
            time.sleep(2)

tasks = [[[1<<7,(1<<2)|(1<<21)],False,False,"prove_black_draws.txt","disprove_black_draws.txt"],
         [[1<<9,(1<<2)|(1<<21)],False,False,"prove_black_draws.txt","disprove_black_draws.txt"],
         [[1<<1,(1<<2)|(1<<21)],False,False,"prove_black_draws.txt","disprove_black_draws.txt"],
         [[(1<<8)|(1<<13)|(1<<21),(1<<2)|(1<<19)|(1<<14)],True,False,"prove_black_draws.txt","disprove_black_draws.txt"],
         [[0,(1<<2)],False,False,"prove_black_draws.txt","disprove_black_draws.txt"],
         [[(1<<8)|(1<<13),(1<<2)|(1<<19)|(1<<14)],False,True,"prove_white_draws.txt","disprove_white_draws.txt"],
         [[0,(1<<2)],False,True,"prove_white_draws.txt","disprove_white_draws.txt"]]
for task in tasks:
    do_a_task(task)

print("ending")
"""replacements(solver.root, None)
print("starting to write to file")
dump_dict(game, solver.root)"""