import os
from sys import argv


script, file_C, file_U, file_p, targetDir, sets_raw_dir = argv

lines_c = open(sets_raw_dir + "set_C_raw/" + file_C, 'r+').readlines()
lines_u = open(sets_raw_dir + "set_U_raw/" + file_U, 'r+').readlines()
lines_p = open(sets_raw_dir + "set_p_raw/" + file_p, 'r+').readlines()


# for openFoam10 indx=21, and for openFoam8 indx=22
# indx <= 32384 for 128*256 images
indx = 21
while indx <= 32385:

    # reading current line in lines_c
    line1 = lines_c[indx]
    line1 = line1.replace('(', '')
    line1 = line1.replace(')', '')
    line1 = line1.split(' ')
    # range line
    line2 = lines_c[indx + 1]
    line2 = line2.replace('(', '')
    line2 = line2.replace(')', '')
    line2 = line2.split(' ')

    # convert few lines to float
    line1_0 = round(float(line1[0]), 2)
    line1_1 = round(float(line1[1]), 2)
    line2_1 = round(float(line2[1]), 2)
    insum = round(line2_1 - line1_1, 2)

    # comparing lines to find empty place (between points)
    if insum != 0.1 and insum != -12.6:
        one_more = str(round((line1_1 + 0.1), 2))  # additional line
        lines_c.insert(indx + 1, '(' + str(line1_0) + ' ' + one_more + " 0)" + '\n')
        lines_u.insert(indx + 1, "(0 0 0)" + '\n')
        lines_p.insert(indx + 1, "0" + '\n')

    indx += 1

with open(targetDir + "set_C_compl/" + file_C, "w+") as f:
    lines_c = "".join(lines_c)
    f.write(lines_c)
f.close()

with open(targetDir + "set_U_compl/" + file_U, "w+") as f:
    lines_u = "".join(lines_u)
    f.write(lines_u)
f.close()

with open(targetDir + "set_p_compl/" + file_p, "w+") as f:
    lines_p = "".join(lines_p)
    f.write(lines_p)
f.close()

print(file_C + " is rdy")
