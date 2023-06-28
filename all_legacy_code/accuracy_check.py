from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import numpy as np
import tensorflow as tf
import sys
import matplotlib.pyplot as plt
import math
import time

sys.path.append('../')
import model.flow_net as flow_net


def locate_largest_absValue(matrix):
    largest_num = 0.0
    row, col, xy = 0, 0, 0
    # ind_col, ind_row = 0, 0
    # matrix = np.reshape(matrix, (32768, 2))

    for ind_row in range(256):
        for ind_col in range(128):
            for ind_xy in range(2):

                number = matrix[ind_row, ind_col, ind_xy]

                if abs(number) > largest_num:
                    largest_num = abs(number)
                    row, col, xy = ind_row, ind_col, ind_xy

    return largest_num, row, col, xy


checkpoint_dir = r"C:\wolk\check_5564_05\\"
# в папке checkpoints есть файл checkpoint,
# в нём в первой строке указывается конкретное поколение

bound_test_dir = r"C:\wolk\sets_less\bnd_upped\\"
flow_test_dir = r"C:\wolk\sets_less\flow_upped\\"

number_of_testFiles = 14                 # how many files is for tests

shape = [128, 256]      # don't use [256, 128] - it's incorrect

##################################

bound_test_files = sorted(os.listdir(bound_test_dir))
flow_test_files = sorted(os.listdir(flow_test_dir))

average_ratio = np.zeros(number_of_testFiles, dtype=np.float32)
max_ratio = []
time_gen = []
num_skipped = 0

for num_file in range(number_of_testFiles):

    print(num_file)
    bound_file = bound_test_dir + bound_test_files[num_file]
    flow_file = flow_test_dir + flow_test_files[num_file]

    with tf.Graph().as_default():

        # Make image placeholder
        boundary_op = tf.compat.v1.placeholder(tf.float32, [1, shape[0], shape[1], 1])

        # Build a Graph that computes the predictions from the inference model.
        sflow_p = flow_net.inference(boundary_op, 1.0)

        # Restore the moving average version of the learned variables for eval.
        variables_to_restore = tf.compat.v1.all_variables()
        saver = tf.compat.v1.train.Saver(variables_to_restore)

        sess = tf.compat.v1.Session()
        ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
        saver.restore(sess, ckpt.model_checkpoint_path)

        boundary_np = np.loadtxt(bound_file, dtype=np.uint8).reshape([1, shape[0], shape[1], 1])
        sflow_true = np.loadtxt(flow_file, dtype=np.float32)
        sflow_true = np.reshape(sflow_true, (256, 128, 2))

        start = time.time()
        sflow_generated = sess.run(sflow_p, feed_dict={boundary_op: boundary_np})[0]
        sflow_generated = np.reshape(sflow_generated, (256, 128, 2))
        time_gen.append(time.time() - start)

        # statistics
        divergence_img = sflow_true - sflow_generated

        sum_true = np.sum(np.absolute(sflow_true))
        sum_gen = np.sum(np.absolute(sflow_generated))
        sum_div = np.sum(np.absolute(divergence_img))

        # average_ratio[num_file] = sum_div / sum_true
        average_ratio[num_file] = sum_gen / sum_true

        # location1 = locate_largest_absValue(divergence_img)
        location1 = locate_largest_absValue(sflow_generated)
        location_true_v = sflow_true[location1[1], location1[2], location1[3]]

        if location_true_v == 0.:
            print("dividing by zero")
            num_skipped += 1
            continue
        else:
            max_ratio.append(location1[0] / abs(location_true_v))

        # plt.imshow(divergence_img[:, :, 0])
        # plt.imshow(sflow_true[:, :, 0])

        # arr1, arr2 = plt.subplots(1, 3)
        # arr2[0].imshow(sflow_true[:, :, 0], vmax=0.5, vmin=-0.5)
        # arr2[1].imshow(sflow_generated[:, :, 0], vmax=0.5, vmin=-0.5)
        # arr2[2].imshow(divergence_img[:, :, 0], vmax=0.5, vmin=-0.5)
        # plt.show()

        # unknown, arr = plt.subplots(2, 3)
        # # arr[0].colorbar(arr[0].imshow(divergence_img[:, :, 0]))
        # arr[0, 0].imshow(divergence_img[:, :, 0], vmin=-0.5, vmax=0.5)
        # # plt.colorbar(arr[0])
        # arr[0, 1].imshow(sflow_generated[:, :, 0], vmin=-0.5, vmax=0.5)
        # # plt.colorbar(arr[1])
        # arr[0, 2].imshow(sflow_true[:, :, 0], vmin=-0.5, vmax=0.5)
        # # plt.colorbar(arr)
        #
        # # arr[0].colorbar(arr[0].imshow(divergence_img[:, :, 0]))
        # di = np.concatenate((divergence_img, np.zeros((256, 128, 1))), axis=2)
        # arr[1, 0].imshow(di, vmin=-0.5, vmax=0.5)
        # # plt.colorbar(arr[0])
        # di = np.concatenate((sflow_generated, np.zeros((256, 128, 1))), axis=2)
        # arr[1, 1].imshow(di, vmin=-0.5, vmax=0.5)
        # # plt.colorbar(arr[1])
        # di = np.concatenate((sflow_true, np.zeros((256, 128, 1))), axis=2)
        # arr[1, 2].imshow(di, vmin=-0.5, vmax=0.5)
        # # plt.colorbar(arr)
        # plt.show()
        # plt.waitforbuttonpress()


print(f"\nnumber of skipped files because if dividing by zero {num_skipped}")

average_ratio_max = round(np.average(max_ratio), 3)    # * 100

all_average_ratio = round(np.average(average_ratio), 3)   # * 100

print(f"\naverage ratio of max_divergence to true_value is:  {average_ratio_max}%")
print(f"largest is:  {round(np.max(max_ratio), 3)}%\n")       # * 100

print(f"average ratio for all points all test images is:  {all_average_ratio}%")
print(f"largest is:  {round(np.max(average_ratio), 3)}%\n")     # * 100

print(f"average time for generation:  {round(np.average(time_gen), 3)}\n")

