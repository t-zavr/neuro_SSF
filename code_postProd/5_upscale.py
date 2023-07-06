import os
import numpy as np
import matplotlib.pyplot as plt


root = r"C:\wolk\5564_set\\"                      # directory WITH BOTH flow_normed and boundary_set
dest_dir = root                                # path to destination directory

normed_flow_path = root + r"flow_normed/"
boundary_path = root + r"bnd_set/"

src_shape = (255, 127)
new_shape = (256, 128)

###################

flow_list = sorted(os.listdir(normed_flow_path))
bnd_list = sorted(os.listdir(boundary_path))

try:
    os.mkdir(dest_dir)
except:
    print("destination path already exist")
try:
    os.mkdir(dest_dir + r"/flow_upped/")
    os.mkdir(dest_dir + r"/bnd_upped/")
except:
    print("path already exist")

os.chdir(root)
for indx in range(len(flow_list)):

    bound = open(boundary_path + bnd_list[indx], 'r').read()
    bound = bound.replace('\n', ' ')
    bound = bound.split(' ')
    bound = bound[:-1]
    bound = [int(n) for n in bound]
    # bound = np.reshape(bound, (src_shape[0] * src_shape[1]))             # reshape to column

    flow = open(normed_flow_path + flow_list[indx], 'r').read()
    flow = flow.replace('\n', ' ')
    flow = flow.split(' ')
    flow = flow[:-1]
    flow = np.array([float(n) for n in flow], dtype=np.float32)
    # flow = np.reshape(flow, (src_shape[0] * src_shape[1], 2))            # reshape to column

    # for line in range(len(bound)):           # making 'zero points' in flow_files again zero (after normalization)
    #     if bound[line] == 1:
    #         flow[line, :] = 0.

    flow = np.reshape(flow, (src_shape[0], src_shape[1], 2))             # reshape back to 256*128
    bound = np.reshape(bound, (src_shape[0], src_shape[1]))
    plt.imshow(flow[:, :, 0])

    new_flow = np.full((new_shape[0], new_shape[1], 2), 0, dtype=np.float32)
    new_bound = np.full(new_shape, 0, dtype=np.int8)

    for y in range(src_shape[0]):
        for x in range(src_shape[1]):
            new_bound[y, x] = bound[y, x]
            new_flow[y, x] = flow[y, x]

    new_flow[new_shape[0] - 1, :] = new_flow[new_shape[0] - 2, :]   # equals to [255, :]=[254, :]
    new_flow[:, 127] = new_flow[:, 126]
    # new_flow[:, 0] = 0.
    plt.imshow(new_flow[:, :, 0])

    new_flow = np.reshape(new_flow, newshape=(new_shape[0] * new_shape[1], 2))   # newshape=(32768, 2)

    # new_bound[:, 0] = 1
    # new_bound[:, new_shape[1] - 1] = 1  # new_array[:, 127] = 1

    np.savetxt(dest_dir + r"flow_upped/" + flow_list[indx], new_flow,
               delimiter=" ", newline="\n", fmt="%s")
    np.savetxt(dest_dir + r"bnd_upped/" + bnd_list[indx], new_bound,
               delimiter=" ", newline="\n", fmt="%s")

    print(bnd_list[indx] + "   is done")
print("all file are done")
