import os
import numpy as np


def imread(path):

    arr = open(path, 'r').read()
    arr = arr.replace(')', '')
    arr = arr.replace('(', '')
    arr = arr.replace("\n", ' ')

    arr = np.fromstring(arr, dtype=float, sep=' ')
    arr = np.reshape(arr, newshape=(16129, 3))

    return arr


rootPath = os.path.dirname(os.path.abspath(__file__))
end_dir = "/mnt/08A8BB59A8BB43CA/zavr/sets/set_rng/"

path_C = rootPath + "/set_C/"
list_C = sorted(os.listdir(path_C))

os.chdir(path_C)
for file_C in list_C:

    imr_file_C = imread(file_C)
    figure_arr = []
    range_arr = ''

    for indx in range(16129):
        if imr_file_C[indx, 2] == 0:
            figure_arr = np.append(figure_arr, [imr_file_C[indx, 0], imr_file_C[indx, 1]])

    for point_indx in range(16129):

        tmp_array = []
        if imr_file_C[point_indx, 2] != 0:

            for fig_indx in range(1, len(figure_arr) - 1, 2):
                Range = ((figure_arr[fig_indx] - imr_file_C[point_indx, 1]) ** 2 +
                         (figure_arr[fig_indx - 1] - imr_file_C[point_indx, 0]) ** 2) ** 0.5
                tmp_array = np.append(tmp_array, round(Range, 10))

            Min = min(tmp_array)
            range_arr = range_arr + str(Min) + '\n'
            # print(str(point_indx) + " indx from 15876 in " + file_C + " is done")

        else:
            range_arr = range_arr + "0\n"
            # print(str(point_indx) + " indx from 15876 was in figure")

    # rootPath + "/set_C/" + file_C
    with open(end_dir + "rng" + file_C[1:], "w+") as f:
        range_arr = "".join(range_arr)
        f.writelines(range_arr)
    f.close()

    print(file_C + " is done")
