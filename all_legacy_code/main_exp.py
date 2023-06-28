import cv2
import os
from distutils.dir_util import copy_tree
# import numpy as np
# import matplotlib.pyplot as plt
# import sys
# from PIL import Image


root = r"C:\Users\280k\Desktop\zavr\try_sff_5.1\dir_exp\\"
files_dir = root + r"blobs_micro_res\\"
fileList = sorted(os.listdir(files_dir))
cavity = root + r"cav123\\"
# cases = root + r"cases\\"
outputPath = cavity + r"system\\"

for file in fileList:

    print(file.split('.')[0])
    inputFile = files_dir + file
    image = cv2.imread(inputFile, 0)

    vertexes0l = []
    vertexes1l = []

    for index_cell, a in enumerate(image):
        for curr_x, b in enumerate(a):
            vertexes0l.append([index_cell, curr_x, 0])
            vertexes1l.append([index_cell, curr_x, 1])

    file1 = open(outputPath + "blockMeshDict", "w")
    # print(outputPath + "blockMeshDict")

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

    # print(x_len)
    # print(y_len)
    for index, _ in enumerate(vertexes0l[:img_len - x_len]):
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
            if index < x_len:
                walls.append([a, a1, d1, d])
            if index > (x_len * (y_len - 2)):
                walls.append([b, b1, c1, c])
            if index % x_len == 0:
                inlet.append([a, b, b1, a1])
            if index % x_len == (x_len - 2):
                outlet.append([c, d, d1, c1])

    # for index_cell, a in enumerate(vertexes0l[:img_len]):
    #
    #     curr_x = index_cell % x_len
    #     curr_y = index_cell // x_len
    #     # print(index_cell, curr_x, curr_y)
    #     if curr_x < x_len - 1 and curr_y < y_len - 1:
    #         if image[curr_x][curr_y] == 255:
    #             front.append([index_cell, index_cell + x_len, index_cell + x_len + 1, index_cell + 1])
    #             back.append([index_cell + img_len, index_cell + x_len + img_len, index_cell + x_len + 1 + img_len,
    #                          index_cell + 1 + img_len])
    #             blocks.append([index_cell, index_cell + x_len, index_cell + x_len + 1, index_cell + 1,
    #                            index_cell + img_len, index_cell + x_len + img_len, index_cell + x_len + 1 + img_len,
    #                            index_cell + 1 + img_len])

    file1.write(""" blocks
    (\n""")
    for b in blocks:
        file1.write(
            "\thex ({} {} {} {} {} {} {} {}) (1 1 1) simpleGrading (1 1 1)\n ".format(b[0], b[1], b[2], b[3], b[4],
                                                                                      b[5], b[6], b[7]))
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
        walls
        {
            type wall;
            faces
            (
    """)
    for p in walls:
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

    # print("file \"{}\" successfully writen".format(outputPath + "blockMeshDict"))

    # fig = plt.figure()
    # ax = fig.gca(projection='3d')

    # plotting the points
    # pts = vertexes0l
    # for number, p in enumerate(pts):
    #     if  image[p[0]][p[1]]!=255:
    #         ax.scatter(p[0], p[1], p[2], zdir='z', c='r')
    #     else:
    #         ax.scatter(p[0], p[1], p[2], zdir='z', c='g')
    #     ax.text(p[0], p[1], p[2], '%s' % (str(number)), size=10, zorder=1,
    #             color='k')
    #
    # plt.show()

    # for indexa, a in enumerate(vertexes0l[:imglen]):

    # # x = []
    # # y = []
    # # nV = np.array(vertexes0l)
    # # for a in vertexes0l:
    # #     x.append(a[0])
    # #     y.append(a[1])
    # # nX = np.array(x)
    # # nY = np.array(y)
    #
    # # print()
    # plt.scatter(nX, nY, marker='.', s=1)
    # plt.show()

    file1.close()

    # copy_tree(cavity, cases + file.split('.')[0])
