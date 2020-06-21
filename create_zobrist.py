import numpy as np
import pickle

white_square_bitstrings = np.random.randint(1<<61,size=9)
black_square_bitstrings = np.random.randint(1<<61,size=9)
empty_square_bitstrings = np.random.randint(1<<61,size=9)
win_pattern_bitstrings = np.random.randint(1<<61,size=(8,9))

with open("zobrist_tik_tac_toe.pkl","wb") as f:
    pickle.dump([white_square_bitstrings,black_square_bitstrings,empty_square_bitstrings,win_pattern_bitstrings],f)