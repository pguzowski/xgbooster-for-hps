import uproot
import numpy as np
import sys

if len(sys.argv) > 1:
  f = uproot.open(sys.argv[1])["kdar"]
  if 'slc' in f:
      b=f['slc'].array("iter")
      print(len(b[b==0]))
  else:
    print('No pot info')
