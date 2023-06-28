import os
from datetime import datetime

# only for files: U, p, rng.
# sets are sorted like: C, U, p, rng.

# makes data_U + data_rng2 (full & hollow data)
sets_path = r"C:\joba_C\sets_framed\\"
path_data = r"C:\joba_C\data_u\\"
hollow_data = r"C:\joba_C\data_rng2\\"

sets_list = sorted(os.listdir(sets_path))
print(sets_list[0], sets_list[1], sets_list[2])

os.mkdir(path_data)
os.mkdir(hollow_data)
list_U = sorted(os.listdir(sets_path + sets_list[0]))
list_p = sorted(os.listdir(sets_path + sets_list[1]))
list_rng = sorted(os.listdir(sets_path + sets_list[2]))

now = datetime.now()
print("start time:  " + str(datetime.now()))

for file_num in range(len(list_rng)):

    name_file = list_p[file_num][1:]
    full_array = []
    hollow_array = []

    os.chdir(sets_path + sets_list[0])
    u = open(list_U[file_num], 'r').readlines()
    # os.chdir(sets_path + sets_list[1])
    # p = open(list_p[file_num], 'r').readlines()
    os.chdir(sets_path + sets_list[2])
    rng = open(list_rng[file_num], 'r').readlines()

    for i in range(16384):
        # f_line = rng[i].replace("\n", '') + " " + p[i].replace("\n", '') \
        #        + " " + u[i].split(' ')[0] + " " + u[i].split(' ')[1] + "\n"      ## 1
        # f_line = rng[i].replace("\n", '') + " " + p[i].replace("\n", '') + "\n"  ## 2
        f_line = rng[i].replace("\n", '') + " " + u[i].split(' ')[0] + " " + u[i].split(' ')[1] + "\n"
        full_array.append(f_line)
        h_line = rng[i].replace("\n", '') + " 0 0" + "\n"
        hollow_array.append(h_line)

    with open(path_data + name_file, "w+") as file:
        full_array = "".join(full_array)
        file.writelines(full_array)
    file.close()
    with open(hollow_data + name_file, "w+") as file:
        hollow_array = "".join(hollow_array)
        file.writelines(hollow_array)
    file.close()

    print(name_file + "   is done")

print("all is done")
print("start time:  " + str(now))
print("end time:   " + str(datetime.now()))
