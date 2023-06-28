import cv2
import os
from distutils.dir_util import copy_tree


root = os.path.abspath(os.getcwd())
cavity = root + r"\cavity\\"

files_dir = r" __ "               # path to directory with png files
cases = r"__ "                    # destination path for cases

################################

for file in sorted(os.listdir(files_dir)):

    print(file.split('.')[0])
    inputFile = files_dir + file
    image = cv2.imread(inputFile, 0)

    vertexes0l = []
    vertexes1l = []

    for index_cell, a in enumerate(image):
        for curr_x, b in enumerate(a):
            vertexes0l.append([index_cell, curr_x, 0])
            vertexes1l.append([index_cell, curr_x, 1])

    file1 = open(cavity + r"system/" + "blockMeshDict", "w")

    file1.write("""FoamFile
    {
        version     2.0;
        format      ascii;
        class       dictionary;
        object      blockMeshDict;
        //date
    }\n""")

    file1.write("""convertToMeters 0.1;
    vertices
    (\n""")

    vertexes0l.extend(vertexes1l)
    for a in vertexes0l:
        file1.write("\t({} {} {})\n".format(a[0], a[1], a[2]))
    file1.write(");\n")

    blocks = []
    front = []
    back = []
    walls = []
    inlet = []
    outlet = []
    y_len = len(image)
    x_len = len(image[0])
    img_len = x_len * y_len

    for index, _ in enumerate(vertexes0l[:img_len - x_len]):

        curr_x = (index % x_len) - x_len
        curr_y = (index // x_len) - x_len
        # if image[curr_x][curr_y] == 255:
        if image[curr_y - 96][curr_x] == 255:

            if index % x_len != (x_len - 1):

                a = index
                b = index + x_len
                c = index + x_len + 1
                d = index + 1
                a1 = index + img_len
                b1 = index + img_len + x_len
                c1 = index + img_len + x_len + 1
                d1 = index + img_len + 1

                front.append([a, d, c, b])
                back.append([a1, b1, c1, d1])
                blocks.append([a, b, c, d, a1, b1, c1, d1])

                # if index % y_len == 0:
                if index < 128:
                    # inlet.append([a, d, b, c])   # alike old
                    inlet.append([a, d, d1, a1])
                    # inlet.append([a, c, c1, a1])

                # if index % y_len == 0:
                if index >= (x_len * (y_len - 2)):
                    outlet.append([c, b, b1, c1])
                    # outlet.append([d, b, b1, d])

    file1.write(""" blocks
    (\n""")
    for b in blocks:
        file1.write(
            "\thex ({} {} {} {} {} {} {} {}) (1 1 1) simpleGrading (1 1 1)\n "
            .format(b[0], b[1], b[2], b[3], b[4], b[5], b[6], b[7]))
    file1.write(");\n")

    file1.write("""
    boundary
    (
        inlet
        {
            type wall;
            faces
            (
    """)
    for p in inlet:
        file1.write("\t({} {} {} {})\n".format(p[0], p[1], p[2], p[3]))
    file1.write("""     );
        }
    """)

    file1.write("""
        outlet
        {
            type wall;
            faces
            (
    """)
    for p in outlet:
        file1.write("\t({} {} {} {})\n".format(p[0], p[1], p[2], p[3]))
    file1.write("""     );
        }
    """)

    file1.write("""
        frontAndBack
        {
            type empty;
            faces
            (
    """)
    for p in front:
        file1.write("\t({} {} {} {})\n".format(p[0], p[1], p[2], p[3]))
    for p in back:
        file1.write("\t({} {} {} {})\n".format(p[0], p[1], p[2], p[3]))
    file1.write("""     );
        }
    );\n""")

    file1.close()
    copy_tree(cavity, cases + file.split('.')[0])
