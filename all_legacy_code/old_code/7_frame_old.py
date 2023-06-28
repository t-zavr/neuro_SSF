import os
import numpy as np
import matplotlib.pyplot as plt


# script for filling the files UP TO new_shape

normed_u_path = r"C:\wolk\set_1+\normed_u\\"
boundary_path = r"C:\wolk\set_1+\boundary\\"
dest_dir = r"C:\wolk\set_1+\dest\\"             # path to destination directory

# script will delete third column in U-files
src_shape = (255, 127)
new_shape = (256, 128)


list_U = sorted(os.listdir(normed_u_path))
bnd_list = sorted(os.listdir(boundary_path))

try:
    os.mkdir(dest_dir)
except:
    print("destination path already exist")
try:
    os.mkdir(dest_dir + r"/set_U_up/")
    os.mkdir(dest_dir + r"/set_bnd_up/")
except:
    print("path already exist")


os.chdir(normed_u_path)
for U in list_U:

    arr = open(U, 'r').read()
    arr = arr.replace('\n', ' ')
    arr = arr.split(' ')
    arr = arr[:-1]

    flow = np.array([float(n) for n in arr], dtype=np.float32)
    flow = np.reshape(flow, (src_shape[0], src_shape[1], 3))
    # flow = np.delete(flow, [2], 2)    # deleting third column

    new_arr = np.full((new_shape[0], new_shape[1], 2), 0, dtype=np.float32)
    for y in range(src_shape[0]):
        for x in range(src_shape[1]):
            new_arr[y, x] = flow[y, x]

    new_arr[new_shape[0]-1, :] = new_arr[new_shape[0]-2, :]   # equals to [255, :]=[254, :]
    new_arr[:, 0] = 0.

    new_arr = np.reshape(new_arr, newshape=(new_shape[0] * new_shape[1], 2))   # newshape=(32768, 2)

    np.savetxt(dest_dir + f"set_U_up/{U}", new_arr,
               delimiter=" ", newline="\n", fmt="%s")

    print(U + "   is done")
print("files U are done")


os.chdir(boundary_path)
for bnd in bnd_list:

    arr = open(bnd, 'r').read()
    arr = arr.replace('\n', ' ')
    arr = arr.split(' ')
    arr = arr[:-1]

    arr = [int(n) for n in arr]
    arr = np.reshape(arr, (src_shape[0], src_shape[1]))

    new_arr = np.full(new_shape, 0, dtype=int)
    for y in range(src_shape[0]):
        for x in range(src_shape[1]):
            new_arr[y, x] = arr[y, x]

    new_arr[:, 0] = 1
    new_arr[:, new_shape[1]-1] = 1     # new_arr[:, 127] = 1

    np.savetxt(dest_dir + r"set_bnd_up/" + "bnd" + bnd[1:], new_arr,
               delimiter=" ", newline="\n", fmt="%s")

    print("bnd" + bnd[1:] + "   is done")
print("files bnd are done")


