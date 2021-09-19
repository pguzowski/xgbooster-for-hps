import uproot
import uproot_methods
#import awkward
import pandas
import numpy as np
import xgboost
from matplotlib import pyplot

#from get_tree import getit
#from model_params import model_params.get_tree as get_tree

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--run","-r", type=int,help="",default=-1)
parser.add_argument("--model","-m", help="",required=True)
parser.add_argument("--max",help="",default=12,type=int)
parser.add_argument("--split_ext_nu",'-s',help="",action='store_true')
args = parser.parse_args()
if args.run != 1 and args.run != 3:
    raise
if args.max < 1:
    raise

from getit_getter import featmap_getter
if args.split_ext_nu:
    featmap_ext = featmap_getter(args.model,'ext')
    featmap_nu = featmap_getter(args.model,'nu')
else:
    featmap = featmap_getter(args.model)
    featmap_ext = featmap
    featmap_nu = featmap

bdt = xgboost.Booster()
bdt.load_model('models/%s/model_r%d.json'%(args.model,args.run))
bdt2 = xgboost.Booster()
bdt2.load_model('models/%s/nu_model_r%d.json'%(args.model,args.run))

#xgboost.plot_importance(bdt,max_num_features=10,featmap='featmaps/featmap_maxextents.txt')
#pyplot.show()

scores = bdt.get_score(fmap=featmap_ext,importance_type='total_gain')

keys = sorted(scores.keys(), key=lambda k: scores[k])

for k in keys[-args.max:]:
    print( k, scores[k])

print('')

scores = bdt2.get_score(fmap=featmap_nu,importance_type='total_gain')

keys = sorted(scores.keys(), key=lambda k: scores[k])

for k in keys[-args.max:]:
    print( k, scores[k])
