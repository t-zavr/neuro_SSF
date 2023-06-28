import os

cases_path = r"C:\wolk\12345\\"


os.chdir(cases_path)
for case in sorted(os.listdir(cases_path)):

    work_file = case + r"/system/controlDict"

    data = open(work_file, 'r').read()
    data = data.replace("startFrom       startTime;", "startFrom       latestTime;")

    work_file = open(work_file, 'w').write(data)

