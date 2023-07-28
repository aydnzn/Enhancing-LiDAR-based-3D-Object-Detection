import argparse
import pickle
import mayavi.mlab as mlab
from tools.visual_utils import visualize_utils as V
import numpy as np
import os

def lidar_to_rect(pts_lidar,V2C_array,R0_array):
    """
    :param pts_lidar: (N, 3)
    :return pts_rect: (N, 3)
    """
    pts_lidar_hom = cart_to_hom(pts_lidar)
    pts_rect = np.dot(pts_lidar_hom, np.dot(V2C_array.T, R0_array.T))
    # pts_rect = reduce(np.dot, (pts_lidar_hom, self.V2C.T, self.R0.T))
    return pts_rect

def cart_to_hom(pts):
    """
    :param pts: (N, 3 or 2)
    :return pts_hom: (N, 4 or 3)
    """
    pts_hom = np.hstack((pts, np.ones((pts.shape[0], 1), dtype=np.float32)))
    return pts_hom

def get_fov_flag(pts_rect, img_shape, P2_array):
    """
    Args:
        pts_rect:
        img_shape:
        calib:

    Returns:

    """
    pts_img, pts_rect_depth = rect_to_img(pts_rect, P2_array)
    val_flag_1 = np.logical_and(pts_img[:, 0] >= 0, pts_img[:, 0] < img_shape[1])
    val_flag_2 = np.logical_and(pts_img[:, 1] >= 0, pts_img[:, 1] < img_shape[0])
    val_flag_merge = np.logical_and(val_flag_1, val_flag_2)
    pts_valid_flag = np.logical_and(val_flag_merge, pts_rect_depth >= 0)

    return pts_valid_flag

def rect_to_img(pts_rect, P2_array):
    """
    :param pts_rect: (N, 3)
    :return pts_img: (N, 2)
    """
    pts_rect_hom = cart_to_hom(pts_rect)
    pts_2d_hom = np.dot(pts_rect_hom, P2_array.T)
    pts_img = (pts_2d_hom[:, 0:2].T / pts_rect_hom[:, 2]).T  # (N, 2)
    pts_rect_depth = pts_2d_hom[:, 2] - P2_array.T[3, 2]  # depth in rect camera coord
    return pts_img, pts_rect_depth

parser = argparse.ArgumentParser(description='Visualize point cloud scenes')
parser.add_argument('--pkl_path', type=str, help='Specify the full path to the pkl file')
parser.add_argument('--extension', type=str, help='Specify the file extension')

args = parser.parse_args()

pkl_path = args.pkl_path
extension = args.extension

# Extract the dataset name from the pkl file path
dataset_name = os.path.basename(os.path.dirname(pkl_path))

with open(pkl_path, 'rb') as f:
    data = pickle.load(f)

for i in range(len(data)):
    lidar_name = data[i]['point_cloud']['lidar_idx']
    lidar_name_with_extension = lidar_name + extension
    gt_box_lidar = data[i]['annos']['gt_boxes_lidar']
    name_lidar = data[i]['annos']['name']
    lidar_file_path = os.path.join(f'./data/{dataset_name}/training/velodyne', lidar_name_with_extension)
    print(lidar_name)
    print(gt_box_lidar)
    if extension == '.bin':
        points = np.fromfile(lidar_file_path, dtype=np.float32).reshape(-1, 4)
    elif extension == '.npy':
        points = np.load(lidar_file_path).astype(np.float32)
    item_numbers = gt_box_lidar.shape[0]
    name_lidar = name_lidar[:item_numbers]
    image_shape = data[i]['image']['image_shape']

    P2_array = data[i]['calib']['P2'][:3, :4]
    R0_array = data[i]['calib']['R0_rect'][:3, :3]
    V2C_array = data[i]['calib']['Tr_velo_to_cam'][:3, :4]

    pts_rect = lidar_to_rect(points[:, 0:3], V2C_array, R0_array)
    fov_flag = get_fov_flag(pts_rect, image_shape, P2_array)
    filtered_points = points[fov_flag]

    V.draw_scenes(points=points, gt_boxes=gt_box_lidar)
    V.draw_scenes(points=filtered_points, gt_boxes=gt_box_lidar)
    mlab.show(stop=True)