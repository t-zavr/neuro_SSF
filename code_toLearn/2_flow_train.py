import os.path
import time
from datetime import datetime

import numpy as np
import tensorflow as tf
import sys

sys.path.append('../')
import model.flow_net as flow_net


train_dir = r" __ "              # directory for checkpoints
from_check = r" __ "

record_file = r" __ .tfrecords"

max_steps = 80001                                   # max number of steps (generations)
batch_size = 8
keep_prob = 0.7                                     # probability for dropout (0.7)
learning_rate = 1e-4

#######################

with tf.Graph().as_default():

    # make inputs
    boundary, sflow = flow_net.inputs(batch_size, record_file)
    # create and unwrap network
    sflow_p = flow_net.inference(boundary, keep_prob)
    # calc error
    error = flow_net.loss_image(sflow_p, sflow)
    # train hopefully
    train_op = flow_net.train(error, learning_rate)
    # List of all Variables
    variables = tf.compat.v1.global_variables()

    # Build a saver
    saver = tf.compat.v1.train.Saver(tf.compat.v1.global_variables())
    # for i, variable in enumerate(variables):
    #  print '----------------------------------------------'
    #  print variable.name[:variable.name.index(':')]

    # Summary op
    summary_op = tf.compat.v1.summary.merge_all()

    # Build an initialization operation to run below.
    init = tf.compat.v1.global_variables_initializer()

    # Start running operations on the Graph.
    sess = tf.compat.v1.Session()

    # init if this is the very time training
    sess.run(init)

    # init from checkpoint
    saver_restore = tf.compat.v1.train.Saver(variables)
    ckpt = tf.train.get_checkpoint_state(from_check)

    if ckpt is not None:
        print("init from " + from_check)
        try:
            saver_restore.restore(sess, ckpt.model_checkpoint_path)
        except:
            tf.compat.v1.gfile.DeleteRecursively(from_check)
            tf.compat.v1.gfile.MakeDirs(from_check)
            print("there was a problem using variables in checkpoint, random init will be used instead")

    # Start que runner
    tf.compat.v1.train.start_queue_runners(sess=sess)

    # Summary op
    graph_def = sess.graph.as_graph_def(add_shapes=True)
    summary_writer = tf.compat.v1.summary.FileWriter(train_dir, graph_def=graph_def)

    for step in range(max_steps):
        t = time.time()
        _, loss_value = sess.run([train_op, error], feed_dict={})
        elapsed = time.time() - t

        assert not np.isnan(loss_value), 'Model diverged with loss = NaN'

        if step % 250 == 0:
            summary_str = sess.run(summary_op, feed_dict={})
            summary_writer.add_summary(summary_str, step)
            print("step number is " + str(step))
            print("loss value at " + str(loss_value))
            print("time per batch is " + str(elapsed))

        if step % 5000 == 0:
            checkpoint_path = os.path.join(train_dir, 'model.ckpt')
            saver.save(sess, checkpoint_path, global_step=step)
            print("saved to " + train_dir)
            print(datetime.now())
