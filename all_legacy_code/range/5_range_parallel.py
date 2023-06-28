import os
import subprocess
import shutil

rootPath = "/mnt/08A8BB59A8BB43CA/zavr/sets/"
range_file = "/mnt/08A8BB59A8BB43CA/zavr/data_x/rangefinder.py"

fileList = sorted(os.listdir(rootPath + "set_C_cut/"))

midPath = rootPath + "mid/"
os.mkdir(midPath)
# targetPath = rootPath + "set_rng/"
# os.mkdir(targetPath)

num_process = 42

if len(fileList) % num_process != 0:
    num_process += 1

i = 0
for np in range(1, num_process + 1):

    # make dirs for parallel work
    dir_set = midPath + "dir_set_" + str(np) + "/"
    os.mkdir(dir_set)
    os.mkdir(dir_set + "set_C/")
    shutil.copy(range_file, dir_set)

    # moving groups of files
    while i < (len(fileList)):
        if i >= (((len(fileList)) // num_process) * np):
            break

        shutil.copy(rootPath + "set_C_cut/" + fileList[i], dir_set + "set_C/")
        print("file was copied   " + fileList[i])
        i += 1


processes = set()
for np in range(1, num_process + 1):
    dir_set1 = midPath + r"dir_set_" + str(np) + "/"
    processes.add(subprocess.Popen(["python3 " + dir_set1 + "rangefinder.py"], shell=True))
    if len(processes) >= num_process:
        os.wait()
        processes.difference_update([p for p in processes if p.poll() is not None])
