import shutil
import os

# script for time = time_point seconds
# user have to set up path to directory with cases & destination directory

cases_dir = " __ "            # directory with cases
dest_dir = " __ "             # destination directory
time_point = r"/120/"     # time_point in cases you want to copy

######################

set_C_path = dest_dir + r"set_C_raw/"
set_U_path = dest_dir + r"set_U_raw/"
set_p_path = dest_dir + r"set_p_raw/"

try:
    os.mkdir(set_C_path)
    os.mkdir(set_U_path)
    os.mkdir(set_p_path)
except:
    print("some destination directory already exist")

# moving data
missed_data = []
fileList = sorted(os.listdir(cases_dir))
for name in fileList:

    try:
        shutil.copy(cases_dir + name + time_point + "C", set_C_path + "C" + name)
        shutil.copy(cases_dir + name + time_point + "U", set_U_path + "U" + name)
        shutil.copy(cases_dir + name + time_point + "p", set_p_path + "p" + name)
        print(name + "  was saved")

    except:
        missed_data = missed_data.append(name)
        print(name + "  was missed")


# writing missed cases in missed.txt
with open(dest_dir + "missed.txt", 'w+') as f:
    f.write(f'cases were missed: \n{len(missed_data)}\n' + missed_data)
