import uproot
import uproot_methods
#import awkward
import pandas
import numpy as np
import xgboost

#from get_tree import getit
#from model_params import model_params.get_tree as get_tree
from getit_getter import getit_getter

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--run","-r", type=int,help="",default=-1)
parser.add_argument("--input","-i", help="",required=True)
parser.add_argument("--output","-o", help="",required=True)
parser.add_argument("--model","-m", help="",required=True)
parser.add_argument("--split_ext_nu",help="",action='store_true')
args = parser.parse_args()
if args.run != 1 and args.run != 3:
    raise


bdt = xgboost.Booster()
bdt.load_model('models/%s/model_r%d.json'%(args.model,args.run))
bdt2 = xgboost.Booster()
bdt2.load_model('models/%s/nu_model_r%d.json'%(args.model,args.run))


fs = uproot.open(args.input)

ts = fs["cand"]

if args.split_ext_nu:
    data_sig_ext = getit_getter(args.model,'ext')(ts)
    data_sig_nu = getit_getter(args.model,'nu')(ts)
    xgb_test_sig = xgboost.DMatrix(data_sig_ext, label=[1]*len(data_sig_ext))
    xgb_test2_sig = xgboost.DMatrix(data_sig_nu, label=[1]*len(data_sig_nu))
    preds_sig = bdt.predict(xgb_test_sig, output_margin=True)
    preds2_sig = bdt2.predict(xgb_test_sig, output_margin=True)
else:
    data_sig_test= getit_getter(args.model)(ts)
    xgb_test_sig = xgboost.DMatrix(data_sig_test, label=[1]*len(data_sig_test))
    preds_sig = bdt.predict(xgb_test_sig, output_margin=True)
    preds2_sig = bdt2.predict(xgb_test_sig, output_margin=True)

with uproot.recreate(args.output) as f:
    f["t"] = uproot.newtree({"bdt_vs_ext": "float64", "bdt_vs_nu": "float64"})
    f["t"].extend({"bdt_vs_ext": preds_sig,"bdt_vs_nu": preds2_sig})

print(args.output,'done')
