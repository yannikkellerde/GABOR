from game_solver import PN_DAG, reconstruct_vicory
from tic_tac_toe import Tic_tac_toe
from qango6x6 import Quango6x6
from data_magic import dump_dict, replacements, save_solution, save_tree_depth, save_sets, save_the_noetigst
import sys
import gc
import time

startpos = [[407423052, 8634042242], True]
game = Quango6x6(startpos)
solver = PN_DAG(game)
solver.loadsets()
while 1:
    res = solver.pn_search()
    save_sets(solver.provenset, solver.disprovenset)
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

    
print("ending")
"""replacements(solver.root, None)
print("starting to write to file")
dump_dict(game, solver.root)"""