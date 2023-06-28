import subprocess
import os


cases_dir = " __ "         # path to computed cases
num_process = 24           # number of processes

time_point = "/120/"       # latest time point in cases, for check if folder exists

###################

file_list = sorted(os.listdir(cases_dir))

processes = set()
for name in file_list:

    workDir = cases_dir + name
    os.chdir(workDir)

    checking = os.path.isdir(workDir + time_point)

    if checking is True:             # check if folder exists
        processes.add(subprocess.Popen(["postProcess -func writeCellCentres -latestTime"],
                                       shell=True))
        print(workDir)

    if len(processes) >= num_process:
        os.wait()
        processes.difference_update([p for p in processes if p.poll() is not None])
