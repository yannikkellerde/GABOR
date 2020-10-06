import numpy as np
import pickle
"""
white_square_bitstrings = np.random.randint(1<<61,size=36)
black_square_bitstrings = np.random.randint(1<<61,size=36)
empty_square_bitstrings = np.random.randint(1<<61,size=36)
win_pattern_bitstrings = np.random.randint(1<<61,size=(61,36))
pattern_score_bitstrings = np.random.randint(1<<61,size=120)
"""

bitstrings = np.random.randint(1<<61,size=120)

with open("zobrist.pkl","wb") as f:
    pickle.dump(bitstrings,f)