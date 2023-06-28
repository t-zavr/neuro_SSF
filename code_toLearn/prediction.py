from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from glob import glob as glb
import numpy as np
import tensorflow as tf
import sys
import matplotlib.pyplot as plt
import imageio as iio
sys.path.append('../')
import model.flow_net as flow_net


# this is script for making a single prediction

checkpoint_dir = r"C:\wolk\check_9383\\"                  # directory with checkpoints

bound_file = r"C:\wolk\sets_more\bnd_upped\bndsquare"       # for boundary files
true_flow = r"C:\wolk\sets_more\flow_upped\flowsquare"

# bound_file = iio.imread(r"C:\wolk\pics_new\re_more_pics\0cat.png", pilmode='1')         # for png files
# bound_file = np.where(bound_file > 0, 0, 1)

#################################

shape = [128, 256]   # don't use [256, 128] - it's incorrect

with tf.Graph().as_default():

    boundary_op = tf.compat.v1.placeholder(tf.float32, [1, shape[0], shape[1], 1])

    sflow_p = flow_net.inference(boundary_op, 1.0)

    variables_to_restore = tf.compat.v1.all_variables()
    saver = tf.compat.v1.train.Saver(variables_to_restore)

    sess = tf.compat.v1.Session()
    ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
    saver.restore(sess, ckpt.model_checkpoint_path)

    true_flow = np.loadtxt(true_flow, dtype=float).reshape((256, 128, 2))
    boundary_np = np.loadtxt(bound_file, dtype=np.uint8).reshape([1, shape[0], shape[1], 1])    # for boundary

    # boundary_np = bound_file.reshape([1, 128, 256, 1])                                        # for png

    sflow_generated = sess.run(sflow_p, feed_dict={boundary_op: boundary_np})[0]
    sflow_generated = np.reshape(sflow_generated, (256, 128, 2))

# true_flow = np.array_split(true_flow, 2)[0]
# sflow_generated = np.array_split(sflow_generated, 2)[0]

picture = np.reshape(boundary_np, (256, 128))
# picture = np.array_split(picture, 2)[0]

divergence_img = true_flow - sflow_generated

# for 4 pictures
unknown, arr = plt.subplots(1, 4)
arr[0].imshow(picture, cmap='Greys')
arr[1].imshow(true_flow[:, :, 1], vmin=-0.35, vmax=0.35)
arr[2].imshow(sflow_generated[:, :, 1], vmin=-0.35, vmax=0.35)
arr[3].imshow(divergence_img[:, :, 1], vmin=-0.35, vmax=0.35)
plt.show()

# # for 2 pictures
# unknown, arr = plt.subplots(1, 2)
# arr[0].imshow(picture, cmap='Greys')
# arr[1].imshow(sflow_generated[:, :, 0], vmin=-0.35, vmax=0.35)
# plt.show()
