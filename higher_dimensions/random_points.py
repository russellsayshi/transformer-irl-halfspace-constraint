import numpy as np

def random_points_on_sphere(n_dimensions, no_points):
    out_arr = np.random.normal(size=(no_points, n_dimensions))
    return out_arr / np.linalg.norm(out_arr, axis=1)[:, np.newaxis]
