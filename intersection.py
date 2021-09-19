import uproot
import numpy as np
import sys

def to_set(fname):
  f = uproot.open(fname)["kdar"]
  st = set()
  if 'pot_tree' in f:
      r = f['pot_tree'].array("run")
      s = f['pot_tree'].array("subrun")
      p = f['pot_tree'].array('pot')
      for i in range(len(r)):
          st.add( (r[i],s[i],p[i]) )
  else:
    raise 'No pot info in file'
  return st

sout = dict()

for fn in sys.argv[1:]:
    s = to_set(fn)
    if 'out' in sout.keys():
        sout['out'] = sout['out'] & s
    else:
        sout['out'] = s

pot_pre = 0
pot_post = 0
if 'out' in sout.keys():
    for x in sout['out']:
        print (x[0],x[1])
        if x[0] < 16880:
            pot_pre += x[2]
        else:
            pot_post += x[2]

print('pot pre:',pot_pre,'post:',pot_post,file=sys.stderr)
