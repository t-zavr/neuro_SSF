import os
import shutil

path_rng = "/mnt/08A8BB59A8BB43CA/zavr/sets/set_rng/"
rng_list = sorted(os.listdir(path_rng))

# mid_path = "/mnt/08A8BB59A8BB43CA/zavr/sets/mid/"
# mid_list = sorted(os.listdir(mid_path))
# dist = "/mnt/08A8BB59A8BB43CA/zavr/sets/Asdf/"

set_c = "/mnt/08A8BB59A8BB43CA/zavr/sets/set_C_cut/"
list_c = sorted(os.listdir(set_c))

miss = []
for i in range(len(rng_list)):

    # k = 0
    # listinmid = sorted(os.listdir(i + "/set_C/"))
    # for k in range(len(listinmid)):
    #     for ind in range(len(rng_list)):
    #         if listinmid[k] == rng_list[ind]:
    #             print(listinmid[k] + "    " + rng_list[ind])
    #             shutil.move(mid_path + i + "/set_C/" + listinmid[k], dist)

    if rng_list[i] != list_c[i]:
        # miss.append(list_c)
        print(list_c[i])
        break
