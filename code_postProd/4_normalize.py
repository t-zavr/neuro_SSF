import numpy as np
import os
from datetime import datetime


root_path = r"C:/wolk/5564_set//"             # path to dir WHICH CONTAINS set_flow directory

flow_dir = root_path + r"/flow_set/"
dest_dir = root_path + r"/flow_normed/"           # destination path for normed set

shape = (32385, 2)    # for 127*255

###########################

now = datetime.now()
print("start at:  " + str(now))

try:
    os.mkdir(dest_dir)
except:
    print("destination dir already exists")

os.chdir(flow_dir)
max_abs_u = []
for file in sorted(os.listdir(flow_dir)):

    u = np.loadtxt(file, dtype=float)
    u = np.abs(u)
    max_abs_u.append(np.max(u))

abs_norma = np.max(max_abs_u)
print("abs norma is " + abs_norma)

for file in sorted(os.listdir(flow_dir)):

    array = np.loadtxt(file, dtype=float)
    array = np.reshape(array, newshape=shape)

    array_normed = array / abs_norma

    np.savetxt(dest_dir + file, array_normed, fmt='%.12f')

print("end time:   " + str(datetime.now()))
