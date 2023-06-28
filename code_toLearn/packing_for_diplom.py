import os
import numpy as np
import tensorflow as tf

flow_dir = r" __ "                       # directory with flow_files
bnd_dir = r"__ "                         # directory with boundary files
train_record_file = ' __ .tfrecords'     # destination of tf file

bnd_list = sorted(os.listdir(bnd_dir))
flow_list = sorted(os.listdir(flow_dir))
train_writer = tf.compat.v1.python_io.TFRecordWriter(train_record_file)

for indx in range(len(bnd_list)):

    bnd_file = bnd_dir + bnd_list[indx]
    flow_file = flow_dir + flow_list[indx]
    
    with open(bnd_file, 'r') as b_file:
        bound = b_file.read()
        b_file.close()
    with open(flow_file, 'r') as f_file:
        flow = f_file.read()
        f_file.close()

    bound = bound.replace('\n', ' ')
    bound = bound.split(' ')
    bound = bound[:-1]
    bound = [str(n) for n in bound]

    flow = flow.replace('\n', ' ')
    flow = flow.split(' ')
    flow = flow[:-1]
    flow = [float(n) for n in flow]

    boundary = np.array(bound, dtype=np.uint8)
    sflow = np.array(flow, dtype=np.float32)
    sflow = sflow.reshape([256, 128, 2])

    b = boundary.tobytes()
    s = sflow.tobytes()
    example = tf.train.Example(features=tf.train.Features(feature={
        'boundary': tf.train.Feature(bytes_list=tf.train.BytesList(value=[b])),
        'sflow': tf.train.Feature(bytes_list=tf.train.BytesList(value=[s]))}))

    train_writer.write(example.SerializeToString())
