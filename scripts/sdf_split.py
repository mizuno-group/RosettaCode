import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("sdffile",help="filename you want to split")
parser.add_argument("-n",dest="N",metavar="N",type=int,default=1000,help="the max number of entries in each splitted file.")
#parser.add_argument("-d",dest="D",metavar="D",help="directory name storing splitted file.")
args = parser.parse_args()

file = args.sdffile
filename, file_extension = os.path.splitext(file)
N = args.N

string = ""
mol_count = 0
file_count = 0
for line in open(file):
    string += line
    if (line.startswith("$$$$")):
        mol_count += 1
        if (mol_count % N == 0):
            file_count += 1
            output = filename+"_"+str(file_count)+".sdf"
            file = open(output,"w")
            file.write(string)
            file.close()
            string = ""

if string != "":
    file_count += 1
    output = filename+"_"+str(file_count)+".sdf"
    file = open(output,"w")
    file.write(string)
    file.close()