import numpy as np
import os
from datetime import datetime
import subprocess
import time


def global_norms(flow_dir, norm_def, norms_file_path, num_process):

    # in norma_def: dir_u_up, file_u, target_file = argv

    list_files = sorted(os.listdir(flow_dir))

    processes = set()
    for flow_file in list_files:

        processes.add(subprocess.Popen(["python3 " + norm_def +
                                        f" {flow_dir} {flow_file} {norms_file_path}"], shell=True))

        if len(processes) >= num_process:
            os.wait()
            processes.difference_update([p for p in processes if p.poll() is not None])

    time.sleep(10)

    norms_file = np.loadtxt(norms_file_path, dtype=float)
    max_global = np.max(norms_file[0:])
    min_global = np.min(norms_file[1:])
    max_abs_global = max(np.absolute(norms_file))
    print("global norms were found at " + str(datetime.now()))

    return max_global, min_global, max_abs_global


root_path = r"C:/wolk/5564_set//"             # path to dir WHICH CONTAINS set_flow directory

flow_dir = root_path + r"/flow_set/"
dest_dir = root_path + r"/flow_normed/"           # destination path for normed set

norms_file_path = root_path + "norms.txt"         # file for norms of every flow_file from the set
norm_def = os.path.abspath(os.getcwd()) + r"/norma_def.py"

num_process = 8
shape = (32385, 2)    # for 127*255

###########################

now = datetime.now()
print("start at:  " + str(now))

try:
    os.mkdir(dest_dir)
except:
    print("destination dir already exists")

os.chdir(flow_dir)
# global_n = global_norms(flow_dir, norm_def, norms_file_path, num_process)
# print(global_n)

max_abs_u = []
for file in sorted(os.listdir(flow_dir)):

    u = np.loadtxt(file, dtype=float)
    u = np.abs(u)
    max_abs_u.append(np.max(u))

abs_norma = np.max(max_abs_u)


for file in sorted(os.listdir(flow_dir)):

    array = np.loadtxt(file, dtype=float)
    array = np.reshape(array, newshape=shape)

    # array_normed = array[:] / global_n[0]                                 # for norm minMax
    # array_normed = (array - global_n[1]) / (global_n[0] - global_n[1])    # for norm 0 to 1
    # array_normed = (2 * ((array - global_n[1]) / (global_n[0] - global_n[1]))) - 1  # for norm -1 to 1
    # array_normed = array / global_n[2]               # for norm -1 to 1

    array_normed = array / abs_norma

    np.savetxt(dest_dir + file, array_normed, fmt='%.12f')

# print("start time:  " + str(now))
print("end time:   " + str(datetime.now()))
