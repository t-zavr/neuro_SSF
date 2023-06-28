import subprocess
import os

# this is script for making boundary- and flow-files in parallel, then saving in <dest_dir>.
# sets_raw_dir - dir with raw data (set_C, set_U).
# def_script - script for every thread.
# def_script can be dedicated for Foam10 (indx=21) or Foam8 (indx=22), check comments there.

work_dir = r" __ "                   # directory with sets C, U
num_process = 24                         # number of processes

def_script = os.path.abspath(os.getcwd()) + r"/ref_def.py"       # path to compl_def.py

#########################

try:
    os.mkdir(work_dir + "/bnd_set/")
    os.mkdir(work_dir + "/flow_set/")
except:
    print("some end_dir already exist")

list_c = sorted(os.listdir(work_dir + r"/set_C_raw/"))
list_u = sorted(os.listdir(work_dir + r"/set_U_raw/"))

os.chdir(work_dir)

processes = set()
for num in range(len(list_c)):

    processes.add(subprocess.Popen(["python3 " + def_script + f" {list_c[num]} {list_u[num]}"
                                    f" {work_dir} {work_dir}"], shell=True))

    if len(processes) >= num_process:
        os.wait()
        processes.difference_update([p for p in processes if p.poll() is not None])

