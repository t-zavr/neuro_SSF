import os

sets_compl_dir = ""  # dir with data after completing
dest_dir = ""        # dir with cuted data

preview = 22
pxls = 32385
# require preview=preview+1 when use openFoam10


path_c = sets_compl_dir + r"/set_C_compl/"
path_u = sets_compl_dir + r"/set_U_compl/"
path_p = sets_compl_dir + r"/set_p_compl/"

list_c = sorted(os.listdir(path_c))
list_u = sorted(os.listdir(path_u))
list_p = sorted(os.listdir(path_p))

try:
    os.mkdir(dest_dir)
except:
    print("target path already exists")
try:
    os.mkdir(dest_dir + r"/set_C_cut/")
    os.mkdir(dest_dir + r"/set_U_cut/")
    os.mkdir(dest_dir + r"/set_p_cut/")
except:
    print("some end_dir already exist")


os.chdir(path_u)
for file in list_u:
    lines = open(file, 'r').readlines()
    lines = lines[preview:]
    lines = lines[:pxls]
    open(dest_dir + "set_U_cut/" + os.path.basename(file), 'w+').writelines(lines)

    text_u = open(dest_dir + "set_U_cut/" + os.path.basename(file), 'r').read()
    text_u = text_u.replace(')', '').replace('(', '')
    # lines = text_u.split('\n')
    open(dest_dir + "set_U_cut/" + os.path.basename(file), 'w+').write(text_u)

    print(file + "   was done")

os.chdir(path_c)
for file in list_c:
    lines = open(file, 'r').readlines()
    lines = lines[preview:]
    lines = lines[:pxls]
    open(dest_dir + "set_C_cut/" + os.path.basename(file), 'w+').writelines(lines)

    text_c = open(dest_dir + "set_C_cut/" + os.path.basename(file), 'r').read()
    text_c = text_c.replace(')', '').replace('(', '')
    open(dest_dir + "set_C_cut/" + os.path.basename(file), 'w+').write(text_c)

    print(file + "   was done")

os.chdir(path_p)
for file in list_p:
    lines = open(file, 'r').readlines()
    lines = lines[preview:]
    lines = lines[:pxls]
    open(dest_dir + "set_p_cut/" + os.path.basename(file), 'w+').writelines(lines)
    print(file + "   was done")
