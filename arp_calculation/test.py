import loader
import linear_programming
from nontrivial_intersections import nontrivial_intersections
import numpy as np
import os

folder = "planedata_fulltraj"

planesets = [loader.load_planes(folder + os.path.sep + filename) for filename in os.listdir(folder)]

for gt_vector, halfspaces_list in planesets:
    #if gt_vector == [0, 0, 0]:
    #    continue
    halfspaces = np.array(halfspaces_list)
    non_redundant_halfspaces, indices = linear_programming.remove_redundant_constraints(halfspaces)
    non, centroid = nontrivial_intersections(non_redundant_halfspaces)
    print(gt_vector / np.linalg.norm(gt_vector), centroid)
