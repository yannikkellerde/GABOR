import sys,os
import pickle

with open(sys.argv[1],"rb") as f:
    s1 = pickle.load(f)

with open(sys.argv[2],"rb") as f:
    s2 = pickle.load(f)

s1.update(s2)
with open(sys.argv[3],"wb") as f:
    pickle.dump(s1,f)