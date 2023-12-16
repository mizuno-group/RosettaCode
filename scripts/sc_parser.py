import pandas as pd
import sys
import argparse

filename = sys.argv[1]
outname = ".".join(filename.split(".")[:-1])

with open(filename,"r") as f:
    sc = f.readlines()

lst = []
for v in sc:
    temp = v.split(" ")
    temp = [v for v in temp if v != ""]
    if temp[0] == "SCORE:":
        lst.append(temp[1:])

df = pd.DataFrame(lst[1:],columns=lst[0][:-1])
df.index = [int(v.split("_")[-1].split("\n")[0]) for v in df[lst[0][-2]]]
df = df.sort_index()
df.to_csv(outname+".csv")

