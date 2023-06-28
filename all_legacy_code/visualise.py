import open3d as o3d
import numpy as np


def read3DArrayFile(name):
    file = open(name, 'r')
    lines = file.readlines()
    data = []
    for index, l in enumerate(lines):
        if index > 0:
            if "boundaryField" in l:
                break
            l = l.replace("(", "").replace(")", "").replace("\n", "")
            try:
                arr = l.split(" ")
                if len(arr) == 3:
                    p = [float(x) for x in arr]
                    data.append(p)
            except Exception:
                print("Error")
    return data


def max_value(inputList):
    return max([max(sublist) for sublist in inputList])


def min_value(inputList):
    return min([min(sublist) for sublist in inputList])


points = read3DArrayFile(r"C:\Users\zavr\Desktop\set_C\C0001_60")
u = read3DArrayFile(r"C:\Users\zavr\Desktop\set_U\U0001_60")
print(max_value(u), min_value(u))

a = np.empty((len(u), 3))
a[:, 2] = 1
u = np.array(u)

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)
pcd.colors = o3d.utility.Vector3dVector(np.array(u) / max_value(u))
# pcd.normals = o3d.utility.Vector3dVector(a)
voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=0.1)
o3d.visualization.draw_geometries([voxel_grid])
