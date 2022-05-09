import numpy as np
import math
from scipy.spatial import ConvexHull
from nontrivial_intersections import nontrivial_intersections
import loader
import linear_programming
import sys

def project_to_plane(plane, vec):
    plane /= np.linalg.norm(plane)
    dt = np.dot(plane, vec)
    return vec - dt * plane

def convex_hull(filename):
    gt_vector, halfspaces_list = loader.load_planes(filename)
    halfspaces = np.array(halfspaces_list)
    non_redundant_halfspaces, indices = linear_programming.remove_redundant_constraints(halfspaces)
    non, centroid = nontrivial_intersections(non_redundant_halfspaces)
    gt_vector /= np.linalg.norm(gt_vector)
    vecs2d = [project_to_plane(gt_vector, x) for x in non]
    planecoord1 = project_to_plane(gt_vector, np.array([2, 14, 23]))
    planecoord1 /= np.linalg.norm(planecoord1)
    planecoord2 = np.cross(gt_vector, planecoord1)
    planecoord2 /= np.linalg.norm(planecoord2)
    plane_to_c3d = np.array([planecoord1, planecoord2, gt_vector]).T
    c3d_to_plane = np.linalg.inv(plane_to_c3d)
    #import code
    #code.interact(local=locals())
    vecs_in_2d = [np.matmul(c3d_to_plane, x)[0:2] for x in vecs2d]
    #print(vecs_in_2d)
    hull = ConvexHull(vecs_in_2d)
    circular_non = [non[x] for x in hull.vertices]
    circular_non.append(circular_non[0])
    return np.array(circular_non), non_redundant_halfspaces, centroid, gt_vector
