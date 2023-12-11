import pandas as pd
import numpy as np
import sys
import subprocess
import argparse
from rdkit import Chem

def calc_center(raw):
    coord = {}
    for i,v in enumerate(raw):
        temp = v.split(" ")
        temp = [w for w in temp if w != ""]
        if temp[0] == "ATOM" or temp[0] == "HETATM":
            #seq = temp[4] + "_" + temp[5]
            d = {}
            d["x"] = float(v[30:38])
            d["y"] = float(v[38:46])
            d["z"] = float(v[46:54])
            coord[i] = d
    coord = pd.DataFrame(coord).T
    center = (np.max(coord,axis=0) + np.min(coord,axis=0)) / 2
    ret = center.values.tolist()
    ret = ",".join([str(np.round(v,2)) for v in ret])
    return ret

def calc_chain_center(raw,chain,save_chain=False):
    coord = {}
    string = ""
    for i,v in enumerate(raw):
        temp = v.split(" ")
        temp = [w for w in temp if w != ""]
        if temp[0] == "HETATM" and temp[4] == chain:
            string += v
            d = {}
            d["x"] = float(v[30:38])
            d["y"] = float(v[38:46])
            d["z"] = float(v[46:54])
            coord[i] = d
    if save_chain == True:
        m = Chem.MolFromPDBBlock(string)
        w = Chem.SDWriter("ligand_chain_{}.sdf".format(chain))
        w.write(m)
            
    coord = pd.DataFrame(coord).T
    center = (np.max(coord) + np.min(coord)) / 2
    ret = center.values.tolist()
    ret = ",".join([str(np.round(v,2)) for v in ret])
    return ret


def main(args):
    with open(args.file,"r") as f:
        raw = f.readlines()
    if args.chain == None:
        ret = calc_center(raw)
    else:
        ret = calc_chain_center(raw,args.chain,args.save_chain)
    return ret


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file",type=str)
    parser.add_argument("--chain",type=str,default=None)
    parser.add_argument("--save_chain",dest="save_chain",action="store_true")
    args = parser.parse_args()

    ret = main(args)
    sys.stdout.write(ret)

