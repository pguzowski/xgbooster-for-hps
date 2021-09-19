import uproot
import numpy as np
import sys

fw= 0.085/0.010563/3.

if len(sys.argv) > 1:
  f = uproot.open(sys.argv[1])["kdar"]
  if 'pot_tree' in f:
    print(np.sum(f['pot_tree'].array("pot"))/fw)
  else:
    print('No pot info')
