import os
import subprocess
from datetime import datetime
import shutil


files_dir = r"/mnt/08A8BB59A8BB43CA/zavr/cases/"
# files_dir = r"C:\wolk\casesTest\\"
files_list = sorted(os.listdir(files_dir))

old_done = r"/mnt/08A8BB59A8BB43CA/zavr/1854_old/done1854/"
destination = r"/mnt/08A8BB59A8BB43CA/zavr/done2/"

indx = 0
for directory in files_list:

    old_check = os.path.isdir(old_done + directory)
    check = files_dir + directory + r"/120/"

    if os.path.isdir(check) is True and old_check is False:
        indx += 1
        print(directory)
        shutil.copytree(files_dir + directory, destination + directory)

print(indx)
