import os

# Для исправления openFoam_9 под 8ую версию

fileList = sorted(os.listdir("cases"))
rootPath = os.path.abspath(os.getcwd())
print(rootPath)

files_list = ["points", "owner", "boundary", "neighbour", "faces"]
files_list_2 = ["p", "phi"]

for dir in fileList:

    for i in files_list:
        workFile = rootPath + "/cases/" + dir + "/constant/polyMesh/" + i
        with open(workFile, 'r') as file:
            data = file.read()
            file.close()
            data = data.replace("""FoamFile
{
    format      ascii;""", """FoamFile
{
    version     2.0;
    format      ascii;""")
            file = open(workFile, 'w')
            file.write(data)
            file.close()
            print('done_1 ' + workFile)

    for z in files_list_2:
        workFile = rootPath + "/cases/" + dir + "/60/" + z
        with open(workFile, 'r') as file:
            data = file.read()
            file.close()
            data = data.replace("""FoamFile
{
    format      ascii;""", """FoamFile
{
    version     2.0;
    format      ascii;""")    
            file = open(workFile, 'w')
            file.write(data)
            file.close()
            print('done_2 ' + workFile)

    workFile = rootPath + "/cases/" + dir + "/60/uniform/time"
    with open(workFile, 'r') as file:
        data = file.read()
        file.close()
        data = data.replace("""FoamFile
{
    format      ascii;""", """FoamFile
{
    version     2.0;
    format      ascii;""")
        file = open(workFile, 'w')
        file.write(data)
        file.close()
        print('done_3 ' + workFile)
