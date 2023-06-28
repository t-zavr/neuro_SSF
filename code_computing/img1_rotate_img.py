import PIL.Image
import os
from PIL import Image

pics_dir = r" __ "      # path to directory with png files
dest_dir = r"__ "       # path to destination directory

list_pics = sorted(os.listdir(pics_dir))

for pic in list_pics:

    original_image = Image.open(pics_dir + pic).convert('1')
    # original_image = original_image.convert('1')

    for deg in range(0, 350, 40):
        original_image.rotate(deg, fillcolor=1,
                              resample=PIL.Image.NEAREST).save(dest_dir + str(deg) + pic)
