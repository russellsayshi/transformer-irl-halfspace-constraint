from collections import defaultdict
import numpy as np
epsilon = 0.000001

def cosine_distance(a, b):
    a = a/np.linalg.norm(a)
    b = b/np.linalg.norm(b)
    cos = np.dot(a, b)
    angle = np.arccos(cos)
    return angle

def calculate_centroid_via_loop(intersections):
    if len(intersections) <= 2:
        raise RuntimeError("<=2 intersections")

    intersections_shifted = intersections[1:]
    intersections_shifted.append(intersections[0])
    intersection_pairs = list(zip(intersections, intersections_shifted))
    
    intersection_sums = [a+b for a, b in intersection_pairs]
    intersection_distances = [cosine_distance(a, b) for a, b in intersection_pairs]
    centroid = sum([distance * intersection_sum for distance, intersection_sum in zip(intersection_distances, intersection_sums)])
    return centroid / np.linalg.norm(centroid)

""" Takes in a numpy array of non-redundant planes with unit normals and returns a numpy array of nontrivial intersections """
def nontrivial_intersections(planes):
    intersections = []

    plane_to_intersections = defaultdict(list)
    intersection_to_planes = []
    last_intersection = None

    intersection_id = 0
    for a_index, a in enumerate(planes):
        for b_index, b in enumerate(planes):
            if (a == b).all():
                continue
            intersection = np.cross(a, b)
            intersection /= np.linalg.norm(intersection)
            multiplied = np.matmul(planes, intersection) + epsilon
            if (multiplied < 0).any():
                continue
            plane_to_intersections[a_index].append((intersection_id, b_index, intersection))
            plane_to_intersections[b_index].append((intersection_id, b_index, intersection))
            intersection_to_planes.append(([a_index, b_index], intersection))
            intersections.append(intersection)
            intersection_id += 1

    centroid = np.zeros_like(planes[0])
    if intersection_id == 0:
        return intersections, centroid

    visited_planes = set()
    current_intersection_id = intersection_id-1
    intersection_loop = []
    visited_planes.add(intersection_to_planes[current_intersection_id][0][1])
    current_plane = intersection_to_planes[current_intersection_id][0][1]
    while True:
        #print(current_intersection_id, "|", current_plane, visited_planes)
        next_planes, _ = intersection_to_planes[current_intersection_id]
        intersection_loop.append(intersections[current_intersection_id])
        assert(len(next_planes) == 2)
        next_plane = None
        if current_plane == next_planes[0]:
            next_plane = next_planes[1]
        elif current_plane == next_planes[1]:
            next_plane = next_planes[0]
        else:
            raise RuntimeError("next_planes does not include current_plane")
        
        if next_plane in visited_planes:
            # We've come full circle
            if len(visited_planes) == len(planes):
                # Celebrate, we have a loop
                print("intersection loop", ", ".join([str(list(x)) for x in intersection_loop]))
                return intersections, calculate_centroid_via_loop(intersection_loop)
            else:
                # We have no loop
                raise RuntimeError("no loop :(")
        else:
            visited_planes.add(next_plane)
            potential_intersections = plane_to_intersections[next_plane]
            assert(len(potential_intersections) == 2)
            next_intersection_id = None
            if potential_intersections[0][0] == current_intersection_id:
                next_intersection_id = potential_intersections[1][0]
            elif potential_intersections[1][0] == current_intersection_id:
                next_intersection_id = potential_intersections[0][0]
            else:
                raise RuntimeError("current_intersection_id is not included in potential_intersections")

            current_intersection_id = next_intersection_id
            current_plane = next_plane

    raise RuntimeError("how did we get here?")

""" Takes in a numpy array of non-redundant planes with unit normals and returns closest point on ARP to pull to """
def closest_point_on_arp(planes, vector):
    #planes = [plane / np.linalg.norm(plane) for plane in planes]
    min_plane_dist = float('infinity')
    min_plane_projected_point = -1
    for plane in planes:
        displacement_to_plane = np.dot(plane, vector)
        projected = vector - displacement_to_plane * plane
        projected /= np.linalg.norm(projected)
        distance_to_plane = np.linalg.norm(projected - vector)
        if distance_to_plane < min_plane_dist:
            min_plane_dist = distance_to_plane
            min_plane_projected_point = projected

    intersections, centroid = nontrivial_intersections(planes)
    min_intersection_dist = float('infinity')
    min_intersection_point = -1
    for intersection in intersections:
        distance = np.linalg.norm(intersection - vector)
        if distance < min_intersection_dist:
            min_intersection_dist = distance
            min_intersection_point = intersection

    if min_intersection_dist < min_plane_dist:
        return min_intersection_point
    else:
        return min_plane_projected_point
