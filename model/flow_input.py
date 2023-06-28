import os
import sys

import numpy as np
import tensorflow as tf
from glob import glob as glb


min_queue_examples = 1000  # min examples to queue up


def read_data(filename_queue, shape):

    reader = tf.compat.v1.TFRecordReader()
    key, serialized_example = reader.read(filename_queue)
    features = tf.io.parse_single_example(
        serialized_example,
        features={
            'boundary': tf.io.FixedLenFeature([], tf.string),
            'sflow': tf.io.FixedLenFeature([], tf.string)
        })
    boundary = tf.io.decode_raw(features['boundary'], tf.uint8)
    sflow = tf.io.decode_raw(features['sflow'], tf.float32)
    boundary = tf.reshape(boundary, [shape[0], shape[1], 1])
    sflow = tf.reshape(sflow, [shape[0], shape[1], 2])
    boundary = tf.compat.v1.to_float(boundary)
    sflow = tf.compat.v1.to_float(sflow)
    sess = tf.compat.v1.Session()
    # with sess.as_default():
        # print(sflow.eval())
    return boundary, sflow


def _generate_image_label_batch(boundary, sflow, batch_size, shuffle=True):
    num_preprocess_threads = 1
    # Create a queue that shuffles the examples, and then
    # read 'batch_size' images + labels from the example queue.
    boundarys, sflows = tf.compat.v1.train.shuffle_batch(
        [boundary, sflow],
        batch_size=batch_size,
        num_threads=num_preprocess_threads,
        capacity=min_queue_examples + 3 * batch_size,
        min_after_dequeue=min_queue_examples)
    return boundarys, sflows


def flow_inputs(batch_size, path_to_records):
    shape = (128, 256)

    # tfrecord_filename = glb('../data/*.tfrecords')
    tfrecord_filename = glb(path_to_records)

    filename_queue = tf.compat.v1.train.string_input_producer(tfrecord_filename)
    boundary, sflow = read_data(filename_queue, shape)

    boundarys, sflows = _generate_image_label_batch(boundary, sflow, batch_size)

    # display in tf summary page
    tf.summary.image('boundarys', boundarys)
    tf.summary.image('sflows_x', sflows[:, :, :, 1:2])
    tf.summary.image('sflows_y', sflows[:, :, :, 0:1])

    return boundarys, sflows
