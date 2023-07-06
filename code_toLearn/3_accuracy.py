from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import numpy as np
import tensorflow as tf
import sys
import matplotlib.pyplot as plt
import time

sys.path.append('../')
import model.flow_net as flow_net


def locate_largest_absValue(matrix):
    largest_num = 0.0
    row, col, xy = 0, 0, 0

    for ind_row in range(256):     # 256
        for ind_col in range(128):
            for ind_xy in range(2):

                number = matrix[ind_row, ind_col, ind_xy]
                if abs(number) > largest_num:
                    largest_num = abs(number)
                    row, col, xy = ind_row, ind_col, ind_xy

    return largest_num, row, col, xy


checkpoint_dir = r" __ "
bound_test_dir = r" __ "
flow_test_dir = r" __ "

##################################

shape = [128, 256]      # don't use [256, 128] - it's incorrect

bound_test_files = sorted(os.listdir(bound_test_dir))
flow_test_files = sorted(os.listdir(flow_test_dir))

average_ratio = np.zeros(len(bound_test_files), dtype=np.float32)
max_ratio = []
time_gen = []
num_skipped = 0
sec_ratio = []

with tf.Graph().as_default():

    boundary_op = tf.compat.v1.placeholder(tf.float32, [1, shape[0], shape[1], 1])
    sflow_p = flow_net.inference(boundary_op, 1.0)
    variables_to_restore = tf.compat.v1.all_variables()
    saver = tf.compat.v1.train.Saver(variables_to_restore)

    sess = tf.compat.v1.Session()
    ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
    saver.restore(sess, ckpt.model_checkpoint_path)

    for num_file in range(len(bound_test_files)):

        print(num_file)
        bound_file = bound_test_dir + bound_test_files[num_file]
        flow_file = flow_test_dir + flow_test_files[num_file]

        boundary_np = np.loadtxt(bound_file, dtype=np.uint8).reshape([1, shape[0], shape[1], 1])
        sflow_true = np.loadtxt(flow_file, dtype=np.float32)
        sflow_true = np.reshape(sflow_true, (256, 128, 2))

        start = time.time()
        sflow_generated = sess.run(sflow_p, feed_dict={boundary_op: boundary_np})[0]
        sflow_generated = np.reshape(sflow_generated, (256, 128, 2))
        time_gen.append(time.time() - start)

        # statistics:

        # sflow_true = np.array_split(sflow_true, 2)[0]
        # sflow_generated = np.array_split(sflow_generated, 2)[0]
        # plt.imshow(sflow_true[:, :, 0])

        divergence_img = sflow_true - sflow_generated

        sum_true = np.sum(np.absolute(sflow_true))
        sum_gen = np.sum(np.absolute(sflow_generated))
        sum_div = np.sum(np.absolute(divergence_img))

        # average_ratio[num_file] = sum_div / sum_true

        sec_div = abs(sum_true - sum_gen)
        sec_ratio.append(sec_div / sum_gen)

        location_maxD = locate_largest_absValue(divergence_img)
        md_gen = (sflow_generated[location_maxD[1], location_maxD[2], location_maxD[3]])
        md_true = (sflow_true[location_maxD[1], location_maxD[2], location_maxD[3]])

        if md_true == 0.:
            print("dividing by zero")
            num_skipped += 1
            continue
        else:
            # max_ratio.append(location_maxD[0] / md_true)
            max_ratio.append( abs(md_true - md_gen) / md_true)

average_ratio_max = round((np.average(max_ratio)) * 100, 3)    # * 100
biggest_ARM = round(np.max(max_ratio) * 100, 3)  # * 100

sec_average_ratio = round(np.average(sec_ratio) * 100, 3)
largest_sec_ratio = round(np.max(sec_ratio) * 100, 3)

print(f"\naverage ratio of max_divergence to true_value:  {str(average_ratio_max)} %")
print(f"largest is:  {str(biggest_ARM)} %")
print(f"number of skipped files because of dividing by zero {num_skipped} \n")

print(f"average ratio for all images:  {str(sec_average_ratio)} %")
print(f"largest ratio is:  {str(largest_sec_ratio)} % \n")

print(f"average time for generation:  {round(np.average(time_gen), 3)}\n")
