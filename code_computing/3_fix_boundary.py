import os
import shutil


files_dir = r" __ "                 # directory with cases

##################################

files_list = sorted(os.listdir(files_dir))

for name in files_list:

    workFile = files_dir + name + "/constant/polyMesh/boundary"

    with open(workFile, 'r') as file:
        data = file.read()
        file.close()

        data = data.replace("""    defaultFaces
    {
        type            empty;""", """    defaultFaces
    {
        type            wall;""")

        file = open(workFile, 'w')
        file.write(data)
        file.close()

#     dict_file = files_dir + name + "/system/controlDict"
#     with open(dict_file, 'r') as file1:
#         data1 = file1.read()
#         file1.close()
#
#         data1 = data1.replace("""stopAt          endTime;
#
# endTime         80;""", """stopAt          endTime;
#
# endTime         120;""")
#
#         data1 = data1.replace("""writeInterval   4000;""",
#                               """writeInterval   6000;""")
#
#         file1 = open(dict_file, 'w')
#         file1.write(data1)
#         file1.close()
