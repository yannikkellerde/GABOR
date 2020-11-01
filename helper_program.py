import os,sys
targ_path = "proofsets/full_game"
os.makedirs(targ_path,exist_ok=True)
start_parts = {}
for fname in os.listdir("proofsets"):
    spart = os.path.join(targ_path,"_".join(fname.split("_")[:-1])+"_"+fname.split("_")[-1][1:])
    if spart in start_parts:
        start_parts[spart].append(os.path.join("proofsets",fname))
    else:
        start_parts[spart] = [os.path.join("proofsets",fname)]
for key,value in start_parts.items():
    command = f"python merge_sets.py {key} "+" ".join(value)
    print(command)
    os.system(command)