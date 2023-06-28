import os
import subprocess
from datetime import datetime


files_dir = r" __ "                # path to dir with cases
time_file = r" __ /time.txt"       # file for writing time of computing

np = 24                            # number of processes (threads)

##################################

now = datetime.now()
processes = set()
files_list = sorted(os.listdir(files_dir))

for name in files_list:

    workDir = files_dir + name
    os.chdir(workDir)

    processes.add(subprocess.Popen(["blockMesh"]))
    if len(processes) >= np:
        os.wait()
        processes.difference_update([p for p in processes if p.poll() is not None])

with open(time_file, "a+") as f:
    f.write(str(now) + '\n' + str(datetime.now()) + '\n')
