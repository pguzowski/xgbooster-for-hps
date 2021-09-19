import uproot
import numpy as np
import sys

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--run","-r", type=int, help="",default=-1)
parser.add_argument("input", help="")
args = parser.parse_args()

fw1 = 0.085/0.010563
fw3 = 0.085/0.0098918330
fw = 1
if args.run == 1:
    fw = fw1
elif args.run == 3:
    fw = fw3

f = uproot.open(args.input)["kdar"]
if 'pot_tree' in f:
    if args.run != 3:
        print(np.sum(f['pot_tree'].array("pot"))/fw)
    else:
        r = f['pot_tree'].array('run')
        print(np.sum(f['pot_tree'].array("pot"))/fw,
                'pre',np.sum(f['pot_tree'].array("pot")[r<16880])/fw,
                'post',np.sum(f['pot_tree'].array("pot")[r>=16880])/fw)
else:
    print('No pot info')
