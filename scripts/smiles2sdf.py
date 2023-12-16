# 220617

from rdkit import Chem
from rdkit.Chem import AllChem
import pandas as pd
from argparse import ArgumentParser

def text2mol(textfile):
    with open(textfile,"r") as tf:
        lst = tf.readlines()
    lst = [v.split()[0] for v in lst]
    mols = []
    for v in lst:
        try:
            m = Chem.MolFromSmiles(v)
            mols.append(m)
        except:
            pass
    return mols, None

def df2mol(file):
    df = pd.read_csv(file,index_col=0)
    mols, index = [], []
    for i,v in zip(df.index,df.values):
        try:
            m = Chem.MolFromSmiles(v)
            mols.append(m)
            index.append(i)
        except:
            pass
    return mols, index

def mol2sdf(lst,savedir,index=None,inonefile=False):
    lst = [AllChem.AddHs(v) for v in lst]
    mols = []
    for v in lst:
        p = AllChem.ETKDGv3()
        AllChem.EmbedMolecule(v,p)
        mols.append(v)
    
    if inonefile == True:
        w = Chem.SDWriter("molecules.sdf")
        for m in mols:
            w.write(m)

    else:
        if index == None:
            for i, v in enumerate(mols):
                [print(Chem.MolToMolBlock(m),file=open("{}/molecule_{}.sdf".format(savedir,i+1),"w+")) for m in mols]
        else:
            for i, v in enumerate(mols):
                [print(Chem.MolToMolBlock(m),file=open("{}/{}.sdf".format(savedir,x),"w+")) for m,x in zip(mols,index)]

def main(args):
    if args.filetype == "df":
        lst, index = df2mol(args.file)
        mol2sdf(lst,args.savedir,index,args.inonefile)
    elif args.filetype == "text":
        lst, _ = text2mol(args.file)
        mol2sdf(lst,args.savedir,None,args.inonefile)
    else:
        raise ValueError()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--filetype",type=str,default="df")
    parser.add_argument("--file",type=str)
    parser.add_argument("--inonefile",dest="inonefile",action="store_true")
    parser.add_argument("--separatefile",dest="inonefile",action="store_false")
    parser.add_argument("--savedir",type=str)
    
    args = parser.parse_args()
    main(args)



