import math

def dot(a, b):
    assert(len(a) == len(b))
    return sum([x*y for x, y in zip(a, b)])

def norm(a):
    return math.sqrt(sum([x*x for x in a]))

def normalize(a):
    length = norm(a)
    return [x/length for x in a]

def load_planes(filename):
    gt_vector = None
    planes = []
    with open(filename, "r") as f:
        firstline = True
        for line in f:
            data = [float(x.strip()) for x in line.strip().split(" ")]
            if firstline:
                gt_vector = data
                firstline = False
            else:
                if dot(data, gt_vector) >= 0:
                    planes.append(normalize(data))
                else:
                    print("WARNING: Skipping misaligned plane")
    return gt_vector, planes
