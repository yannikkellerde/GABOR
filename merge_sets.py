import sys,os
import pickle

s = set()
for fname in sys.argv[2:]:
    with open(fname,"rb") as f:
        s.update(pickle.load(f))
        
with open(sys.argv[1],"wb") as f:
    pickle.dump(s,f)