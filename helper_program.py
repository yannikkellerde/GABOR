import os,sys
from collections import defaultdict
targ_fol = "all_p_set"
targ_path = os.path.join("proofsets/",targ_fol)
os.makedirs(targ_path,exist_ok=True)
start_parts = defaultdict(list)
for folder in os.listdir("proofsets"):
    if folder==targ_fol:
        continue
    for fname in ("bd.pkl","bp.pkl","wd.pkl","wp.pkl"):
        spart = os.path.join(targ_path,fname)
        start_parts[spart].append(os.path.join("proofsets",folder,fname))
for key,value in start_parts.items():
    command = f"python merge_sets.py {key} "+" ".join(value)
    print(command)
    os.system(command)