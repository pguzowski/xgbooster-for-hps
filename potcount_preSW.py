import uproot
import numpy as np
import sys

if len(sys.argv) > 1:
  f = uproot.open(sys.argv[1])["kdar"]
  if 'pot_tree' in f:
    r = f['pot_tree'].array('run')
    print(np.sum(f['pot_tree'].array("pot")[r<16880]))
  else:
    print('No pot info')
