import os
import subprocess
from datetime import datetime


files_dir = r"/mnt/08A8BB59A8BB43CA/zavr/cases/"
time_file = r"/mnt/08A8BB59A8BB43CA/zavr/time.txt"
files_list = sorted(os.listdir(files_dir))

np = 24
threshold, num_cases = 135, np * 1

# indx = 0
# number = 0
# for directory in files_list:
#
#     # check = files_dir + directory + r"/120/"
#     check2 = files_dir + directory + r"/30/"
#
#     if os.path.isdir(check2) is False:
#         number += 1
#
#         if number > threshold:
#             indx += 1
#             list_for_run.append(directory)
#
#             if indx == 1 * np:
#                 break

list_for_run = []
dir_index, threshold_itr = 0, 0
while len(list_for_run) < num_cases:

    # check = files_dir + directory + r"/120/"
    check = files_dir + files_list[dir_index] + r"/30/"

    if os.path.isdir(check) is False:
        threshold_itr += 1
        if threshold_itr > threshold:
            list_for_run.append(files_list[dir_index])

    dir_index += 1

print(len(list_for_run))
print(list_for_run)

####################

now = datetime.now()
processes = set()
for name in list_for_run:
    workDir = files_dir + name
    os.chdir(workDir)
    processes.add(subprocess.Popen(["icoFoam"]))
    if len(processes) >= np:
        os.wait()
        processes.difference_update([p for p in processes if p.poll() is not None])

with open(time_file, "a+") as f:
    f.write(str(now) + '\n' + str(datetime.now()) + '\n')
