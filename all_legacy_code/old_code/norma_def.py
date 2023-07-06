import numpy as np
import os
from sys import argv

script, flow_dir, flow_file, target_file = argv

os.chdir(flow_dir)

u = np.loadtxt(flow_file, dtype=float)
max_u = np.max(u)
min_u = np.min(u)

with open(target_file, "a+") as f:
    f.write(str(max_u) + " " + str(min_u) + '\n')
