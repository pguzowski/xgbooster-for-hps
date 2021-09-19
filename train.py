import uproot
import uproot_methods
#import awkward
import pandas
import numpy as np
import xgboost

#from get_tree import getit, featmap
#from model_params import model_params as params
#getit = params.getit
#featmap = params.featmap

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--run","-r", type=int, help="",default=-1)
parser.add_argument("--num_round","-n", type=int, help="",default=300)
parser.add_argument("--model","-m",help="",required=True)
parser.add_argument("--split_ext_nu",help="",action='store_true')
args = parser.parse_args()
if args.run != 1 and args.run != 3:
    raise
if args.num_round < 1:
    raise

from getit_getter import params_getter

params = params_getter(args.model, 'ext' if args.split_ext_nu else None)
getit = params.getit
featmap = params.featmap

class run:
    pass

r1 = run()
r1.sig = "../signals/to_bdt/training_fhc.root"
r1.cos = "../backgrounds/to_bdt/ana_ext_r1_train.root"
#r1.cos_test = "../backgrounds/to_bdt/ana_ext_r1_test.root"
r1.neut = "../backgrounds/to_bdt/ana_nu_fhc_r1_train.root"
r1.num = 1

r3 = run()
r3.sig = "../signals/to_bdt/training_rhc.root"
r3.cos = "../backgrounds/to_bdt/ana_ext_r3_train.root"
#r3.cos_test = "../backgrounds/to_bdt/ana_ext_r3_test.root"
r3.neut = "../backgrounds/to_bdt/ana_nu_rhc_r3_train.root"
r3.num = 3

r13 = r3 if args.run == 3 else r1



fs = uproot.open(r13.sig)
fc = uproot.open(r13.cos)
#fc_test = uproot.open(r13.cos_test)
fn = uproot.open(r13.neut)

ts = fs["cand"]
tc = fc["cand"]
#tc_test = fc_test["cand"]
tn = fn["cand"]

#data_sig = ts.arrays("*", namedecode="utf-8")
data_sig = getit(ts)
#data_sig_masses = ts.pandas.df("true_mass")


##### PG NEW TRAIN 10_up
#data_cos_train = getit(tc)
#data_cos_test = getit(tc_test)
#################
data_cos = getit(tc)
data_cos_train = data_cos[:int(len(data_cos)*.7)]
data_cos_test = data_cos[int(len(data_cos)*.7):]

data_nu = getit(tn)
data_nu_test = data_nu[int(len(data_nu)*.7):]

#print(data_sig.columns)
#print(data_cos.head(2))
#print(xx)

data_sig_train = data_sig[:int(len(data_sig)*.7)]
data_sig_test = data_sig[int(len(data_sig)*.7):]

labels = [1]*len(data_sig_train) + [0]*len(data_cos_train)

#scale = float(len(data_sig_train))/float(len(data_cos_train))
#weights = [1]*len(data_sig_train) + [scale]*len(data_cos_train)
#weights = [1]*len(data_sig_train) + [scale]*len(data_cos_train)

print('len train sig',len(data_sig_train),'cos',len(data_cos_train))
print('len test sig',len(data_sig_test),'cos',len(data_cos_test),'nu',len(data_nu_test))

#print(xx)

xgb_train = xgboost.DMatrix(pandas.concat([data_sig_train, data_cos_train]), label=labels)
xgb_test_sig = xgboost.DMatrix(data_sig_test, label=[1]*len(data_sig_test))
xgb_test_ext = xgboost.DMatrix(data_cos_test, label=[0]*len(data_cos_test))
xgb_test_nu = xgboost.DMatrix(data_nu_test, label=[0]*len(data_nu_test))

watchlist = [(xgb_train, 'train'), (xgb_test_sig, 'test_sig'),(xgb_test_ext,'test_ext'),(xgb_test_nu,'test_nu')]
param = params.param
num_round = args.num_round

bdt = xgboost.train(param, xgb_train, num_round, watchlist)

bdt.save_model('models/%s/model_r%d.json'%(params.name,r13.num))

bdt.dump_model('models/%s/dump_r%d.raw.txt'%(params.name,r13.num),featmap)
