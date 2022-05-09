import random_points
import numpy as np

"""
    Approximates the centroid of a set of planes on the surface of an n_dimensional sphere

    Arguments
        planes: array of normal vectors representing planes passing through the origin
        accuracy: [-1,1] maximum cosine distance between any two of the necessary_samples most recent samples along the surface of the sphere before we stop the algorithm
        necessary_samples: how many previous samples for accuracy calculation
        too_many_random_samples: arbitrary high number, used to stop the loop if we still don't find a good random sample after this many tries
"""
def approximate_centroid(planes, accuracy=0.9999, necessary_samples=32, too_many_random_samples=100000):
    assert(len(planes.shape) == 2)
    n_dimensions = planes.shape[1]

    """ Finds a random point within the plane boundary """
    # TODO find a more efficient way to do this than trial-and-error
    def next_random_point():
        i = 0
        while i < too_many_random_samples:
            point = random_points.random_points_on_sphere(n_dimensions, 1)[0]
            if (np.matmul(planes, point) >= 0).all():
                return point
        raise RuntimeError("Unable to find a suitable point after " + str(too_many_random_samples) + " samples.")

    samples = np.zeros((necessary_samples, n_dimensions), dtype=planes.dtype)
    current_points_sum = np.zeros((n_dimensions,), dtype=planes.dtype)
    n_samples = 0
    while n_samples < necessary_samples or np.matmul(samples, samples.T).min() < accuracy:
        current_points_sum += next_random_point()
        current_sample = current_points_sum / np.linalg.norm(current_points_sum)
        samples[n_samples % necessary_samples] = current_sample
        n_samples += 1
    print(f"Took {n_samples}")
    return samples[(n_samples-1) % necessary_samples]

points = [[-0.6032552936255785, -0.5838850080012555, -0.5432875372618913], [-0.5636865527421199, -0.6514193287983118, -0.5078487258285309], [-0.495384539307263, -0.680869619784045, -0.539454093570955], [-0.504298744141982, -0.6104784631113569, -0.6107362955760984], [-0.5844888374279835, -0.5657533246679675, -0.5816321643007939]]
planes = np.array(points)
import time
start = time.time()
centroids = [approximate_centroid(planes) for _ in range(10)]
end = time.time()
print(f"Took {end-start} seconds.")
