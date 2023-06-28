import os
from PIL import Image


# this script puts the 128*128 picture into white(empty) 128*256 picture

directory = r" __ "                  # path to directory with png files
dest_dir = r" __ "                   # path to destination directory

src_shape = (128, 128)
dst_shape = (128, 256)

####################################

files_list = sorted(os.listdir(directory))

try:
    os.makedirs(dest_dir)
except:
    print("destination exists")

background = Image.new('RGBA', dst_shape, (255, 255, 255, 255))
offset = (0, 50)      # (0, dst_shape[0] - src_shape[0] // 2)

os.chdir(directory)
for file in files_list:

    image = Image.open(file, 'r')
    background.paste(image, offset)
    background.save((dest_dir + file))

