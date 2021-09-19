import uproot

#from get_tree import getit, featmap_vars
from getit_getter import getit_featmapvars_getter
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--model","-m", help="",required=True)
parser.add_argument("--split_ext_nu", help="",default=None)
args = parser.parse_args()
getit, featmap_vars = getit_featmapvars_getter(args.model,args.split_ext_nu)

sig = "../signals/to_bdt/training_fhc.root"

fs = uproot.open(sig)["cand"]

df = getit(fs)

for i,c in enumerate(df.columns):
    t=None
    for k in featmap_vars.keys():
        if c in featmap_vars[k]:
            t = k
            break
    if t is None:
        raise t
    print(i,c,t)
