from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re
from glob import glob as glb

import numpy as np
import tensorflow as tf

from absl import app  # new
import sys

sys.path.append('../')

import model.flow_net as flow_net
from test.flow_reader import load_flow, load_boundary
from model.experiment_manager import make_checkpoint_path

import matplotlib.pyplot as plt

# FLAGS = tf.app.flags.FLAGS
FLAGS = tf.compat.v1.flags.FLAGS

tf.compat.v1.flags.DEFINE_string('base_dir', '../checkpoints',
                                 """dir to store trained net """)
tf.compat.v1.flags.DEFINE_integer('batch_size', 8,
                                  """ training batch size """)
tf.compat.v1.flags.DEFINE_integer('max_steps', 60001,                  # 500000
                                  """ max number of steps to train """)
tf.compat.v1.flags.DEFINE_float('keep_prob', 0.7,
                                """ keep probability for dropout """)
tf.compat.v1.flags.DEFINE_float('learning_rate', 1e-4,
                                """ keep probability for dropout """)
tf.compat.v1.flags.DEFINE_bool('display_test', True,
                               """ display the test images """)

TEST_DIR = make_checkpoint_path(FLAGS.base_dir, FLAGS)
TEST_DIR = r"C:\wolk\point120k\\"

def tryint(s):
    try:
        return int(s)
    except:
        return s


def alphanum_key(s):
    return [tryint(c) for c in re.split('([0-9]+)', s)]


def evaluate():
    """Run Eval once.
  """
    # get a list of image filenames
    filenames = glb('../data/computed_car_flow/*/')
    filenames.sort(key=alphanum_key)
    filename_len = len(filenames)
    shape = [128, 256]

    with tf.Graph().as_default():
        # Make image placeholder
        boundary_op = tf.compat.v1.placeholder(tf.float32, [1, shape[0], shape[1], 1])

        # Build a Graph that computes the logits predictions from the
        # inference model.
        sflow_p = flow_net.inference(boundary_op, 1.0)

        # Restore the moving average version of the learned variables for eval.
        variables_to_restore = tf.compat.v1.all_variables()
        saver = tf.compat.v1.train.Saver(variables_to_restore)

        sess = tf.compat.v1.Session()

        ckpt = tf.train.get_checkpoint_state(TEST_DIR)

        saver.restore(sess, ckpt.model_checkpoint_path)
        global_step = 1

        graph_def = tf.compat.v1.get_default_graph().as_graph_def(add_shapes=True)

        for run in filenames:
            # read in boundary
            flow_name = run + '/fluid_flow_0002.h5'
            boundary_np = load_boundary(flow_name, shape).reshape([1, shape[0], shape[1], 1])
            sflow_true = load_flow(flow_name, shape)

            # calc logits
            sflow_generated = sess.run(sflow_p, feed_dict={boundary_op: boundary_np})[0]

            if FLAGS.display_test:
                # convert to display
                sflow_plot = np.concatenate([sflow_true, sflow_generated, sflow_true - sflow_generated], axis=1)
                boundary_concat = np.concatenate(3 * [boundary_np], axis=2)
                sflow_plot = np.sqrt(
                    np.square(sflow_plot[:, :, 0]) + np.square(sflow_plot[:, :, 1])) - .05 * boundary_concat[0, :, :, 0]

                # display it
                plt.imshow(sflow_plot)
                plt.colorbar()
                plt.show()


def main(argv=None):  # pylint: disable=unused-argument
    evaluate()


if __name__ == '__main__':
    # tf.app.run()
    app.run(main)
