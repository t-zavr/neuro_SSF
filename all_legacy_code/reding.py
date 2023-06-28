import tensorflow as tf
import numpy as np


# этот скрипт сохраняет один example в файл

# filenames = "/mnt/08A8BB59A8BB43CA/zavr/try_sff_7.3/data/train.tfrecords"
# destination = "/mnt/08A8BB59A8BB43CA/zavr/try_sff_7.3/exp_dir/"

# filename = r"C:\wolk\train.tfrecords"
filename = r"C:\wolk\experiment4.tfrecords"
destination = r"C:\Users\becza\OneDrive\net_walks\try_sff_7.4.1\exp_dir\\"

# C:\Users\becza\OneDrive\net_walks\try_sff_7.4.1\exp_dir\

raw_dataset = tf.data.TFRecordDataset(filename)
for raw_record in raw_dataset.take(1):
    example = tf.train.Example()
    example.ParseFromString(raw_record.numpy())

with open(destination + "2new.txt", 'w+') as file:
    file.write(str(example))
file.close()
