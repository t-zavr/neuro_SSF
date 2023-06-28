"""Builds the ring network.

  # Compute pics of the simulation running.
  
  # Create a graph to train on.
"""

import tensorflow as tf
# import numpy as np
import model.flow_architecture as flow_architecture
import model.flow_input as flow_input

FLAGS = tf.compat.v1.flags.FLAGS

# Constants describing the training process.
tf.compat.v1.flags.DEFINE_string('model', 'res',
                                 """ model name to train """)
tf.compat.v1.flags.DEFINE_integer('nr_res_blocks', 1,
                                  """ nr res blocks """)
tf.compat.v1.flags.DEFINE_bool('gated_res', True,
                               """ gated resnet or not """)
tf.compat.v1.flags.DEFINE_string('nonlinearity', 'concat_elu',
                                 """ nonlinearity used such as concat_elu, elu, concat_relu, relu """)


def inputs(batch_size, record_file):
    boundary, sflow = flow_input.flow_inputs(batch_size, record_file)
    return boundary, sflow


def inference(boundary, keep_prob):
    if FLAGS.model == "res":
        sflow_p = flow_architecture.conv_res(boundary, nr_res_blocks=FLAGS.nr_res_blocks, keep_prob=keep_prob,
                                             nonlinearity_name=FLAGS.nonlinearity, gated=FLAGS.gated_res)

    return sflow_p


def loss_image(sflow_p, sflow):
    loss = tf.nn.l2_loss(sflow_p - sflow)
    tf.summary.scalar('loss', loss)
    return loss


def train(total_loss, lr):
    train_op = tf.compat.v1.train.AdamOptimizer(lr).minimize(total_loss)
    return train_op
