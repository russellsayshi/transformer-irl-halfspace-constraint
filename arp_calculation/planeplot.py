import numpy as np
import math
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
from mpl_toolkits.mplot3d import Axes3D # <--- This is important for 3d plotting
from nontrivial_intersections import nontrivial_intersections
import loader
import linear_programming

def project_to_plane(plane, vec):
    plane /= np.linalg.norm(plane)
    dt = np.dot(plane, vec)
    return vec - dt * plane

gt_vector, halfspaces_list = loader.load_planes('planedata_fulltraj_gridworld/normal_vectors_positive_neutral_negative.txt')
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
#[np.matmul(plane_to_c3d, [x[0], x[1], 0]) for x in vecs_in_2d]
#import code
#code.interact(local=locals())
#print(gt_vector / np.linalg.norm(gt_vector), centroid)

# plot the surface
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')

u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x = np.cos(u)*np.sin(v)
y = np.sin(u)*np.sin(v)
z = np.cos(v)
ax.plot_wireframe(x, y, z, color="b", alpha=0.2, zorder=-10)

# draw a point
#ax.scatter([0], [0], [0], color="g", s=100)

# draw a vector
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d


class Arrow3D(FancyArrowPatch):

    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)

x = np.linspace(-5,5,2)
y = np.linspace(-5,5,2)
z = np.linspace(-5,5,2)

X,Y = np.meshgrid(x,y)
random.shuffle(halfspaces)
right = 0
total = 0
for normal_vector in halfspaces[0:5]:
  print(normal_vector)
  Z = -(normal_vector[0] * X + normal_vector[1] * Y)/normal_vector[2]
  length = math.sqrt(sum([x * x for x in normal_vector])) * 0.5
  normal_vector[0] = normal_vector[0] / length
  normal_vector[1] = normal_vector[1] / length
  normal_vector[2] = normal_vector[2] / length
  right += 1 if np.dot(normal_vector, gt_vector) >= 0 else 0
  total += 1
  print(normal_vector)
  print(length)
  #a = Arrow3D([0, normal_vector[0]], [0, normal_vector[1]], [0, normal_vector[2]], mutation_scale=10,
  #            lw=1, arrowstyle="-|>", color="k")
  #ax.add_artist(a)
  #ax.plot_surface(X, Y, Z, alpha=0.1)

print('right, total', right, total)

ax.axes.set_xlim3d(left=-1, right=1)
ax.axes.set_ylim3d(bottom=-1, top=1)
ax.axes.set_zlim3d(bottom=-1, top=1)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_box_aspect([1,1,1])

#ax.plot([gt_vector[0]*5], [gt_vector[1]*5], [gt_vector[2]*5], markerfacecolor='b', markeredgecolor='b', marker='o', markersize=20, alpha=1)

#for a in non:
#    for b in non:
#        #ax.plot([x[0] for x in non], [x[1] for x in non], zs=[x[2] for x in non], markerfacecolor='b', markeredgecolor='b', marker='o', markersize=1, alpha=1, zorder=100)
#        ax.plot([a[0], b[0]], [a[1], b[1]], zs=[a[2], b[2]], markerfacecolor='b', markeredgecolor='b', marker='o', markersize=1, alpha=1, zorder=10, color='b')
##ax.plot([x[0] for x in non], [x[1] for x in non], zs=[x[2] for x in non], markerfacecolor='b', markeredgecolor='b', marker='o', markersize=0, alpha=1, zorder=100)

ax.view_init(elev=25, azim=-62)

ax.plot([x[0] for x in circular_non], [x[1] for x in circular_non], zs=[x[2] for x in circular_non], markerfacecolor='r', markeredgecolor='r', marker='o', markersize=0, alpha=1, zorder=-5, color='r')

ax.scatter([gt_vector[0]], [gt_vector[1]], [gt_vector[2]], color="g", s=15, zorder=0)
ax.scatter([centroid[0]], [centroid[1]], [centroid[2]], color="y", s=15, zorder=0)

plt.xticks(np.arange(-1, 1.1, 0.5))
plt.yticks(np.arange(-1, 1.1, 0.5))


plt.savefig('polytope.svg', format='svg')
plt.show()
