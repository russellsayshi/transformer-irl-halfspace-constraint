import numpy as np

epsilon = 0.001

def test_redundancy(original_set, new_set, num_tests=1000):
    assert(original_set.shape[1] == new_set.shape[1])
    assert(new_set.shape[0] <= original_set.shape[0])
    for _ in range(num_tests):
        points = np.random.normal(size=(original_set.shape[1]))
        points = points / np.linalg.norm(points)
        ov = np.matmul(original_set, points)
        nv = np.matmul(new_set, points)
        in_old = True
        in_new = True
        unknown = False
        for old, new in zip(ov, nv):
            if old < epsilon and old > -epsilon:
                unknown = True
                break
            if new < epsilon and new > -epsilon:
                unknown = True
                break
            
            old_positive = old > 0
            new_positive = new > 0
            if not old_positive:
                in_old = False
            if not new_positive:
                in_new = False
        if not unknown and (in_old != in_new):
            return False
    return True

a = test_redundancy(np.array([[1, 2, 3], [3, 4, -5]]), np.array([[1, 2, 3]]))
