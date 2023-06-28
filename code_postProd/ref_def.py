from sys import argv
import numpy as np


script, file_C, file_U, dest_dir, sets_raw_dir = argv

lines_c = open(sets_raw_dir + "set_C_raw/" + file_C, 'r+').readlines()
lines_u = open(sets_raw_dir + "set_U_raw/" + file_U, 'r+').readlines()

preview, num_lines = 22, int(lines_c[20])                      # for openFoam8
shape = (255, 127)

bound, flow = [], []

lines_c = lines_c[preview:]
lines_c = lines_c[:num_lines]
lines_u = lines_u[preview:]
lines_u = lines_u[:num_lines]
# flow = flow[:-1]

c_arr = [str(n).replace('(', '').replace(')', '').replace('\n', '').split(' ') for n in lines_c]
c_arr = np.reshape(c_arr, (num_lines * 3))
u_arr = [str(n).replace('(', '').replace(')', '').replace('\n', '').split(' ') for n in lines_u]
u_arr = np.reshape(u_arr, (num_lines * 3))

c_arr = [float(n) for n in c_arr]
c_arr = np.reshape(c_arr, (num_lines, 3))
u_arr = [float(n) for n in u_arr]
u_arr = np.reshape(u_arr, (num_lines, 3))

for indx in range(num_lines - 1):

    sum_parameter = round((c_arr[indx+1, 1] - c_arr[indx, 1]), 2)

    if sum_parameter != 0.1 and sum_parameter != -12.6:

        sum_parameter *= 10
        for num in range(int(sum_parameter)):
            bound.append([1])
            flow.append([0.0, 0.0])

    else:

        bound.append([0])
        flow.append([u_arr[indx, 0], u_arr[indx, 1]])

bound.append([0])
flow.append([u_arr[num_lines-1, 0], u_arr[num_lines-1, 1]])

bound = np.reshape(bound, shape)
np.savetxt(dest_dir + r"bnd_set/bnd" + file_C[1:], bound,
           delimiter=" ", newline="\n", fmt="%s")

np.savetxt(dest_dir + r"flow_set/flow" + file_C[1:], flow,
           delimiter=" ", newline="\n", fmt="%s")

print(file_C + " is done")
