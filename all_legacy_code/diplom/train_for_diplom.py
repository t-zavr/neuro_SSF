import os.path
import numpy as np
import tensorflow as tf
import sys

sys.path.append('../../')
import model.flow_net as flow_net


train_dir = r" __ "              # directory for checkpoints
record_file = r" __ .tfrecords"

max_steps = 80001              # max number of steps (generations)
batch_size = 8
keep_prob = 0.7                # probability for dropout (0.7)
learning_rate = 1e-4

with tf.Graph().as_default():

    boundary, sflow = flow_net.inputs(batch_size, record_file)
    sflow_p = flow_net.inference(boundary, keep_prob)
    error = flow_net.loss_image(sflow_p, sflow)
    train_op = flow_net.train(error, learning_rate)
    variables = tf.compat.v1.global_variables()

    saver = tf.compat.v1.train.Saver(tf.compat.v1.global_variables())
    summary_op = tf.compat.v1.summary.merge_all()

    init = tf.compat.v1.global_variables_initializer()
    sess = tf.compat.v1.Session()
    sess.run(init)

    tf.compat.v1.train.start_queue_runners(sess=sess)
    graph_def = sess.graph.as_graph_def(add_shapes=True)
    summary_writer = tf.compat.v1.summary.FileWriter(train_dir, graph_def=graph_def)

    for step in range(max_steps):
        _, loss_value = sess.run([train_op, error], feed_dict={})

        assert not np.isnan(loss_value), 'Model diverged with loss = NaN'

        if step % 250 == 0:
            summary_str = sess.run(summary_op, feed_dict={})
            summary_writer.add_summary(summary_str, step)
            print(f"at step  {str(step)}  loss value is {str(loss_value)}")

        if step % 5000 == 0:
            checkpoint_path = os.path.join(train_dir, 'model.ckpt')
            saver.save(sess, checkpoint_path, global_step=step)
