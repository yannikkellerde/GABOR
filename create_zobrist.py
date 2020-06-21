import numpy as np
import pickle

white_square_bitstrings = np.random.randint(1<<61,size=36)
black_square_bitstrings = np.random.randint(1<<61,size=36)
empty_square_bitstrings = np.random.randint(1<<61,size=36)
win_pattern_bitstrings = np.random.randint(1<<61,size=(61,36))

with open("zobrist_hashs.pkl","wb") as f:
    pickle.dump([white_square_bitstrings,black_square_bitstrings,empty_square_bitstrings,win_pattern_bitstrings],f)