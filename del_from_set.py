import sys,os
import pickle

with open(sys.argv[1],"rb") as f:
    s = pickle.load(f)

for h in sys.argv[2:]:
    s.remove(int(h))

with open(sys.argv[1],"wb") as f:
    pickle.dump(s,f)