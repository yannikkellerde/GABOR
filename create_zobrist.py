import numpy as np
import pickle

white_square_bitstrings = np.random.randint(1<<61,size=36)
black_square_bitstrings = np.random.randint(1<<61,size=36)
empty_square_bitstrings = np.random.randint(1<<61,size=36)
win_pattern_bitstrings = np.random.randint(1<<61,size=(61,36))
pattern_score_bitstrings = np.random.randint(1<<25,size=100)

with open("zobrist_qango6x6.pkl","wb") as f:
    pickle.dump([white_square_bitstrings,black_square_bitstrings,empty_square_bitstrings,win_pattern_bitstrings,pattern_score_bitstrings],f)