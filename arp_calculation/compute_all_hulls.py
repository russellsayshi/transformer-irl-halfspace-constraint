import get_convex_hull
import numpy as np
import os

def gt_to_str(x):
    ret = []
    for i in x:
        if i < 0:
            ret.append('negative')
        elif i == 0:
            ret.append('neutral')
        else:
            ret.append('positive')
    return '_'.join(ret)

environment_names = ['gridworld', 'spaceinvaders', 'miner', 'dodgeball']
folder_prefix = 'planedata_fulltraj_'

out_folder = 'processed_planes'
if not os.path.exists(out_folder):
    os.mkdir(out_folder)
processed_prefix = out_folder + os.path.sep

for environment_name in environment_names:
    subfolder_name = processed_prefix + environment_name
    if not os.path.exists(subfolder_name):
        os.mkdir(subfolder_name)
    files = os.listdir(folder_prefix + environment_name)
    for filename in files:
        path = folder_prefix + environment_name + os.path.sep + filename
        print(path)
        if path[-3:] != 'txt':
            continue
        if 'neutral_neutral_neutral' in path:
            continue
        save_prefix = subfolder_name + os.path.sep + filename[15:-4]
        if os.path.exists(save_prefix + '.npy'):
            continue
        assert(filename[:14] == 'normal_vectors')
        print(' ', path)
        try:
            convex_hull, planes, centroid, gt_vector = get_convex_hull.convex_hull(path)
            if environment_name == 'spaceinvaders' or environment_name == 'gridworld':
                for first_index in range(3):
                    remaining_indices = list(range(3))
                    remaining_indices = remaining_indices[0:first_index] + remaining_indices[first_index+1:]
                    for second_index in remaining_indices:
                        third_index = 3 - first_index - second_index
                        indices = (first_index, second_index, third_index)
                        mod_hull = convex_hull[:, indices]
                        mod_name = gt_to_str(gt_vector[(indices,)]) #'_'.join(np.array(filename[15:-4].split("_"))[indices,])
                        mod_centroid = centroid[indices,]
                        mod_planes = planes[:, indices]
                        mod_save_prefix = subfolder_name + os.path.sep + mod_name
                        np.save(mod_save_prefix + '.npy', {'hull': mod_hull, 'centroid': mod_centroid, 'planes': mod_planes})
            else:
                np.save(save_prefix + '.npy', {'hull': convex_hull, 'centroid': centroid, 'planes': planes})
        except Exception as e:
            print(e)
