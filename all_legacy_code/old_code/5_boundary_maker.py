import os
import numpy as np
from datetime import datetime


set_C_cut_dir = r""        # path to directory with set_C_cut
dest_dir = r""             # destination path for boundarys
src_shape = (255, 127)     # shape of source files (set_C_cut)


try: 
    os.makedirs(dest_dir)
except:
    print("destination exists")

now = datetime.now()

list_c = sorted(os.listdir(set_C_cut_dir))
os.chdir(set_C_cut_dir)

for file_C in list_c:
   
    lines_c = open(file_C, 'r+').readlines()    
    numbers = []

    for line in lines_c:

        line = line.replace('\n', ' ')
        line = line.split(' ')

        if float(line[2]) == 0.:
            numbers.append(1)
        else:
            numbers.append(0)

    # reshape from column to picture
    numbers = np.reshape(numbers, src_shape)

    np.savetxt(dest_dir + file_C, numbers,
               delimiter=" ", newline="\n", fmt="%s")
    print(file_C)

print("start time:  " + str(now))
print("end time:   " + str(datetime.now()))
