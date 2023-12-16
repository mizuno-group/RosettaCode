import pandas as pd
import sys
import argparse
import os
import glob
import numpy as np

def main(args):
    ps = glob.glob(args.path+"/*")
    ps2 = glob.glob(args.path+"_dock/*")
    filenames = ["/".join(v.split("/")[-2:]) for v in ps]
    ps2_conf = set(["_".join(v.split("_")[:-1]) for v in ps2])

    remain_list = []
    for x in ps2_conf:
        conc = []
        for y in glob.glob(x+"*"):
            dat = pd.read_csv(y,index_col=0)
            conc.append(dat)
        # 落とし方の条件は要検討
        if args.criteria == "interface":
            concated = pd.concat(conc,axis=0).sort_values(by="interface_delta_X")[:args.number]
        elif args.criteria == "total":
            concated = pd.concat(conc,axis=0).sort_values(by="total_score")[:args.number]
        else:
            concated = pd.concat(conc,axis=0).sort_values(by="total_score")[:args.number*3]
            concated = concated.sort_values(by="interface_delta_X")[:args.number]
        desc = concated["description"].values.tolist()
        remain_list.extend(desc)
        concated.to_csv(x+"_remain.csv")
    
    lst = [v[:-1] + ".pdb" for v in remain_list]
    remove_list = [v for v in filenames if v not in lst]
    for v in remove_list:
        os.remove(v)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--score_path",type=str,default=os.getcwd()+"/output")
    parser.add_argument("--criteria",type=str,default="total")
    parser.add_argument("--number",type=int,default=10)
    args = parser.parse_args()
    main(args)