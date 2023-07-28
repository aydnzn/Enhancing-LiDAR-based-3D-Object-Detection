import pandas as pd
import numpy as np
import os
import glob
import open3d
import sys
import visualize_utils as V_mayavi
import mayavi.mlab as mlab
import copy

def expand_or_adjust_obb(obb_test, points, object_name):
    # Get the center, rotation matrix, and extents of the original OBB
    C = np.array(obb_test.center)
    R = np.array(obb_test.R)
    S = np.array(obb_test.extent)

    # Transform points to the coordinate system of the OBB
    P_transformed = (np.linalg.inv(R) @ (points - C).T).T

    # Compute the min and max coordinates of the transformed points
    min_coords = np.min(P_transformed, axis=0)
    max_coords = np.max(P_transformed, axis=0)

    # Compute the center and size of the point cloud in the OBB coordinate system
    P_center = (min_coords + max_coords) / 2
    P_size = max_coords - min_coords

    # Flag to indicate whether the OBB was expanded
    expanded = False

    # If the object is a pedestrian or bicycle
    if 'PED' in object_name or 'BIC' in object_name: 
        # If the OBB is smaller than the point cloud along any axis, expand it
        for i in range(3):
            if S[i] < P_size[i]:
                # The new size is the size of the point cloud along this axis
                S[i] = P_size[i]
                # Flag that the OBB was expanded
                expanded = True

    # If the OBB was expanded, recompute its center
    if expanded:
        C_new = (min_coords + max_coords) / 2
        C = (R @ C_new) + C
    # If the OBB wasn't expanded but the object is a pedestrian or bicycle, adjust its center in the xy-plane
    else:
        if 'PED' in object_name or 'BIC' in object_name:
            C_new_ped = (R @ np.array([P_center[0], P_center[1], 0])) + C
            C = np.array([C_new_ped[0], C_new_ped[1], obb_test.center[2]])

    # Update the original OBB with new center and extents
    obb_test.center = C
    obb_test.extent = S
    
    # Return the updated OBB
    return obb_test



def generate_points_in_obb(obb_fnc, num_points):
    """
    Generate a set of random points within a specified Oriented Bounding Box (OBB).

    :param obb_fnc: The Oriented Bounding Box
    :param num_points: Number of points to generate within the OBB
    :return translated_points: The generated points
    """
    # Generate random points directly within the OBB, considering its extent
    points = np.random.uniform(-0.5 * obb_fnc.extent, 0.5 * obb_fnc.extent, size=(num_points, 3))

    # Transform the points to align with the orientation of the OBB
    transformed_points = np.dot(points, obb_fnc.R.T)

    # Translate the points to match the center of the OBB
    translated_points = transformed_points + obb_fnc.center[np.newaxis, :]

    return translated_points



def lidar_to_rect(pts_lidar,V2C_array,R0_array):
    """
    Transforms points from LiDAR coordinates to rectified coordinates

    :param pts_lidar: points in LiDAR coordinates (N, 3)
    :return pts_rect: points in rectified coordinates (N, 3)
    """
    pts_lidar_hom = cart_to_hom(pts_lidar)  # Convert to homogeneous coordinates
    # Perform coordinate transformation
    pts_rect = np.dot(pts_lidar_hom, np.dot(V2C_array.T, R0_array.T))
    return pts_rect

def cart_to_hom(pts):
    """
    Converts points from Cartesian coordinates to homogeneous coordinates

    :param pts: points in Cartesian coordinates (N, 3 or 2)
    :return pts_hom: points in homogeneous coordinates (N, 4 or 3)
    """
    pts_hom = np.hstack((pts, np.ones((pts.shape[0], 1), dtype=np.float32)))  # Append ones along the second axis
    return pts_hom

def get_fov_flag(pts_rect, img_shape, P2_array):
    """
    Check if the rectified points fall within the image boundaries

    Args:
        pts_rect: points in rectified coordinates
        img_shape: shape of the image
        P2_array: Camera matrix

    Returns:
        pts_valid_flag: Boolean array indicating the validity of each point
    """
    pts_img, pts_rect_depth = rect_to_img(pts_rect, P2_array)  # Project points onto image plane
    # Check if the points fall within the image boundaries
    val_flag_1 = np.logical_and(pts_img[:, 0] >= 0, pts_img[:, 0] < img_shape[1])
    val_flag_2 = np.logical_and(pts_img[:, 1] >= 0, pts_img[:, 1] < img_shape[0])
    val_flag_merge = np.logical_and(val_flag_1, val_flag_2)
    # Check if the depth of the points is non-negative
    pts_valid_flag = np.logical_and(val_flag_merge, pts_rect_depth >= 0)
    return pts_valid_flag

def rect_to_img(pts_rect, P2_array):
    """
    Project points from rectified coordinates onto an image plane

    :param pts_rect: points in rectified coordinates (N, 3)
    :return pts_img: projected points in image coordinates (N, 2)
    """
    pts_rect_hom = cart_to_hom(pts_rect)  # Convert to homogeneous coordinates
    pts_2d_hom = np.dot(pts_rect_hom, P2_array.T)  # Project points onto image plane
    pts_img = (pts_2d_hom[:, 0:2].T / pts_rect_hom[:, 2]).T  # Normalize by depth
    pts_rect_depth = pts_2d_hom[:, 2] - P2_array.T[3, 2]  # Calculate depth in rectified camera coordinates
    return pts_img, pts_rect_depth

def filter_point_cloud(point_cloud, range_values):
    """
    Filters the point cloud based on a provided range along the x, y, and z axis

    :param point_cloud: The point cloud to be filtered (N, 3)
    :param range_values: A list of range values [x_min, y_min, z_min, x_max, y_max, z_max]
    :return flag_array: Boolean array indicating whether each point falls within the specified range
    """
    x_min, y_min, z_min, x_max, y_max, z_max = range_values
    x, y, z = point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2]
    
    # Create boolean array indicating whether each point falls within the specified range
    flag_array = np.logical_and.reduce((x >= x_min, x <= x_max, y >= y_min, y <= y_max, z >= z_min, z <= z_max))
    
    return flag_array



def get_optimal_oriented_bounding_box(car_df,extents, object_name,pcd_fov):
    """
    Compute the optimal Oriented Bounding Box for an object given the object's point cloud and extents.
    The optimal OBB is the one that contains the maximum number of points from the point cloud's FOV.

    :param car_df: DataFrame containing the object's point cloud
    :param extents: Dictionary mapping each object name to its extents
    :param object_name: Name of the object
    :param pcd_fov: Point cloud of the FOV
    :return best_obb: The optimal OBB
    :return az_selected: The azimuth corresponding to the optimal OBB
    """
    x_values = car_df.values[:,0]
    y_values = car_df.values[:,1]
    z_values = car_df.values[:,2]                       
    az = car_df.values[:,5]  # Azimuths of the points
    
    extent = extents[object_name]  # Extents of the object
    distance = extent[0]/2  # Half the length of the object
    x_values_moved = x_values + np.cos(az)*distance  # x-coordinates of the OBB centers
    y_values_moved = y_values + np.sin(az)*distance  # y-coordinates of the OBB centers

    max_points_inside = 0  # Maximum number of points inside an OBB
    best_obb = None  # The optimal OBB
    az_selected = None  # Azimuth corresponding to the optimal OBB
    prev_distance = float('inf')  # Set an initial value for prev_distance
    for i in range((len(x_values))):
        center = [x_values_moved[i], y_values_moved[i], z_values[i]]  # Center of the OBB
        lwh = extent  # Length, width, and height of the OBB
        axis_angles = np.array([0, 0, az[i] + 1e-10])  # Orientation of the OBB
        rot = open3d.geometry.get_rotation_matrix_from_axis_angle(axis_angles)  # Rotation matrix for the OBB
        obb_10 = open3d.geometry.OrientedBoundingBox(center, rot, lwh)  # Construct the OBB
        distance_to_origin = np.sqrt(center[0]**2 + center[1]**2 )  # Distance from the OBB center to the origin
        points_inside = obb_10.get_point_indices_within_bounding_box(pcd_fov.points)  # Indices of points from the FOV that fall within the OBB
        num_points_inside = len(points_inside)  # Number of points inside the OBB
        if num_points_inside > max_points_inside:  # If the OBB contains more points than the current optimal OBB
            max_points_inside = num_points_inside
            best_obb = obb_10
            az_selected = az[i]
        elif num_points_inside == max_points_inside:  # If the OBB contains the same number of points as the current optimal OBB
            is_moving_towards_origin = distance_to_origin < prev_distance  # Check if the OBB center is closer to the origin than the current optimal OBB
            if is_moving_towards_origin:  # If it is, update the optimal OBB
                max_points_inside = num_points_inside
                best_obb = obb_10
                az_selected = az[i]

        prev_distance = distance_to_origin  # Update the distance to the origin

    return best_obb, az_selected


def calculate_truncation_ratio(obb_expanded, num_points,V2C_array,R0_array,image_shape, P2_array):
    """
    Calculate the truncation ratio for an expanded Oriented Bounding Box.

    :param obb_expanded: The expanded Oriented Bounding Box
    :param num_points: Number of points to generate within the OBB
    :param V2C_array: Array for transformation from Velodyne coordinates to camera coordinates
    :param R0_array: Rectification matrix
    :param image_shape: Shape of the image (height, width)
    :param P2_array: Projection matrix
    :return truncation: Truncation ratio
    """
    hypothetical_point_cloud = generate_points_in_obb(obb_expanded, num_points)  # Generate a hypothetical point cloud within the OBB
    hyp_pts_rect = lidar_to_rect(hypothetical_point_cloud[:, 0:3],V2C_array,R0_array)  # Transform the point cloud to rectified camera coordinates
    hyp_fov_flag = get_fov_flag(hyp_pts_rect, image_shape, P2_array)  # Determine which points fall within the FOV
    hyp_filtered_points = hypothetical_point_cloud[hyp_fov_flag]  # Filter the points that fall within the FOV
    truncation = 1 - hyp_filtered_points.shape[0]/hypothetical_point_cloud.shape[0]  # Calculate the truncation ratio

    return truncation



def generate_kitti_label(best_bbox, P2_array, R0_array, V2C_array, image_shape, truncation, Type):
    """
    Generate a label string in the KITTI dataset format for a given Oriented Bounding Box (OBB).

    :param best_bbox: The best bounding box (OBB)
    :param P2_array: Projection matrix
    :param R0_array: Rectification matrix
    :param V2C_array: Transformation from Velodyne coordinates to camera coordinates
    :param image_shape: Shape of the image (height, width)
    :param truncation: Truncation value of the object
    :param Type: The type of the object
    :return line: The generated label string
    """
    # Some lengthy code to transform the OBB to camera coordinates and to compute the 2D and 3D bounding boxes in image and camera coordinates
    best_bbox = np.array(best_bbox)
    boxes3d_lidar_copy = copy.deepcopy(best_bbox)
    boxes3d_lidar_copy = np.array(boxes3d_lidar_copy)
    xyz_lidar = boxes3d_lidar_copy[:, 0:3]
    l, w, h = boxes3d_lidar_copy[:, 3:4], boxes3d_lidar_copy[:, 4:5], boxes3d_lidar_copy[:, 5:6]
    r = boxes3d_lidar_copy[:, 6:7]
    xyz_lidar[:, 2] -= h.reshape(-1) / 2
    pts_lidar_hom = cart_to_hom(xyz_lidar)
    xyz_cam = np.dot(pts_lidar_hom, np.dot(V2C_array.T, R0_array.T))
    r = -r - np.pi / 2
    best_boxes_camera = np.concatenate([xyz_cam, l, h, w, r], axis=-1)
    boxes3d = best_boxes_camera
    bottom_center = True
    boxes_num = boxes3d.shape[0]
    l, h, w = boxes3d[:, 3], boxes3d[:, 4], boxes3d[:, 5]
    x_corners = np.array([l / 2., l / 2., -l / 2., -l / 2., l / 2., l / 2., -l / 2., -l / 2], dtype=np.float32).T
    z_corners = np.array([w / 2., -w / 2., -w / 2., w / 2., w / 2., -w / 2., -w / 2., w / 2.], dtype=np.float32).T
    if bottom_center:
        y_corners = np.zeros((boxes_num, 8), dtype=np.float32)
        y_corners[:, 4:8] = -h.reshape(boxes_num, 1).repeat(4, axis=1)  # (N, 8)
    else:
        y_corners = np.array([h / 2., h / 2., h / 2., h / 2., -h / 2., -h / 2., -h / 2., -h / 2.], dtype=np.float32).T

    ry = boxes3d[:, 6]
    zeros, ones = np.zeros(ry.size, dtype=np.float32), np.ones(ry.size, dtype=np.float32)
    rot_list = np.array([[np.cos(ry), zeros, -np.sin(ry)],
                        [zeros, ones, zeros],
                        [np.sin(ry), zeros, np.cos(ry)]])  # (3, 3, N)
    R_list = np.transpose(rot_list, (2, 0, 1))  # (N, 3, 3)

    temp_corners = np.concatenate((x_corners.reshape(-1, 8, 1), y_corners.reshape(-1, 8, 1),
                                z_corners.reshape(-1, 8, 1)), axis=2)  # (N, 8, 3)
    rotated_corners = np.matmul(temp_corners, R_list)  # (N, 8, 3)
    x_corners, y_corners, z_corners = rotated_corners[:, :, 0], rotated_corners[:, :, 1], rotated_corners[:, :, 2]

    x_loc, y_loc, z_loc = boxes3d[:, 0], boxes3d[:, 1], boxes3d[:, 2]

    x = x_loc.reshape(-1, 1) + x_corners.reshape(-1, 8)
    y = y_loc.reshape(-1, 1) + y_corners.reshape(-1, 8)
    z = z_loc.reshape(-1, 1) + z_corners.reshape(-1, 8)

    corners = np.concatenate((x.reshape(-1, 8, 1), y.reshape(-1, 8, 1), z.reshape(-1, 8, 1)), axis=2)
    corners3d =corners.astype(np.float32)

    pts_rect_hom = cart_to_hom(corners3d.reshape(-1, 3))
    pts_2d_hom = np.dot(pts_rect_hom, P2_array.T)
    pts_img = (pts_2d_hom[:, 0:2].T / pts_rect_hom[:, 2]).T  # (N, 2)
    corners_in_image = pts_img.reshape(-1, 8, 2)
    min_uv = np.min(corners_in_image, axis=1)  # (N, 2)
    max_uv = np.max(corners_in_image, axis=1)  # (N, 2)
    boxes2d_image = np.concatenate([min_uv, max_uv], axis=1)
    if image_shape is not None:
        boxes2d_image[:, 0] = np.clip(boxes2d_image[:, 0], a_min=0, a_max=image_shape[1] - 1)
        boxes2d_image[:, 1] = np.clip(boxes2d_image[:, 1], a_min=0, a_max=image_shape[0] - 1)
        boxes2d_image[:, 2] = np.clip(boxes2d_image[:, 2], a_min=0, a_max=image_shape[1] - 1)
        boxes2d_image[:, 3] = np.clip(boxes2d_image[:, 3], a_min=0, a_max=image_shape[0] - 1)
    
    best_boxes_img=boxes2d_image  
    # Compute alpha, the rotation angle in image plane
    alpha = -np.arctan2(-best_bbox[:, 1], best_bbox[:, 0]) + best_boxes_camera[:, 6]

    # Extract relevant values for the KITTI label
    bbox = best_boxes_img
    dimensions = best_boxes_camera[:, 3:6]
    location = best_boxes_camera[:, 0:3]
    rotation = best_boxes_camera[:, 6]
    truncated = truncation
    occluded = np.full((best_bbox.shape[0], 1), 0)  # Here, it assumes that the object is not occluded

    # Generate the KITTI label string
    line = f"{Type} {truncated:.2f} {int(occluded)} {alpha[0]} " \
        f"{bbox[0][0]} {bbox[0][1]} {bbox[0][2]} {bbox[0][3]} " \
        f"{dimensions[0][1]} {dimensions[0][2]} {dimensions[0][0]} " \
        f"{location[0][0]} {location[0][1]} {location[0][2]} {rotation[0]}\n"

    return line


def process_pointcloud_data(modified_dir,file,P2_array, R0_array,V2C_array,image_shape,extents,df,time_carmaker):
    # Initializing red_flag which might be used to signal errors or exceptions during execution
    red_flag = False
    point_cloud_file = file

    # Extracting the timestamp from the file name
    time_ms = int(point_cloud_file.split('_')[1])
    time_s = time_ms / 1000

    # Generating corresponding label and contributions file names
    label_file = file.replace("pointcloud", "label").replace(".npy", ".txt")
    contributions_file = file.replace("pointcloud.npy", "contributions.txt")

    # Fetching the row in the dataframe that corresponds to the current timestamp
    index = time_carmaker[(time_carmaker.iloc[:,0] <= time_s)  & (time_carmaker.iloc[:,0] >= (time_s-0.1)) ].index
    row = df.iloc[index]

     # Loading point cloud data
    points = np.load(os.path.join(modified_dir, point_cloud_file))

    # Loading and processing file contributions
    with open(os.path.join(chosen_subdir, contributions_file), 'r') as file_2:
        file_contents = file_2.read()

    # filter out empty lines in the contributions file and removes the corresponding points in the point cloud.
    my_lines = file_contents.splitlines()
    empty_indexes = np.where(np.array(my_lines) == '')[0]
    my_lines = np.delete(my_lines, empty_indexes)
    points = np.delete(points, empty_indexes, axis=0)
    points = np.array(points)

    # Transforming the point cloud from lidar coordinates to rectified camera coordinates
    pts_rect = lidar_to_rect(points[:, 0:3],V2C_array,R0_array)
    # Getting the flags that represent whether each point is in the field of view or not
    fov_flag = get_fov_flag(pts_rect, image_shape, P2_array)

    # Filtering points and lines based on the field of view and point cloud range
    filtered_points = points[fov_flag]
    flag_array = filter_point_cloud(filtered_points, POINT_CLOUD_RANGE)
    filt_filt_points = filtered_points[flag_array]

    # Note: The same filtering process is done to the lines as well
    filtered_lines = list(filter(lambda x: x[1], zip(my_lines, fov_flag)))
    filtered_lines = [line for line, flag in filtered_lines]
    filt_filt_lines = list(filter(lambda x: x[1], zip(filtered_lines, flag_array)))
    filt_filt_lines = [line for line, flag in filt_filt_lines]

    # Creating dictionaries to hold point cloud data and lines grouped by objects
    indices_by_object = {}
    indices_by_object_raw = {}


    for obj, obj_values in objects.items():
        obj_values_set = set(obj_values)
        obj_indices = np.array([index for index, line in enumerate(filt_filt_lines) if int(line.split()[0]) in obj_values_set])
        obj_indices_raw = np.array([index for index, line in enumerate(my_lines) if int(line.split()[0]) in obj_values_set])
        indices_by_object[obj] = obj_indices
        indices_by_object_raw[obj] = obj_indices_raw

    points_by_object = {obj: [filt_filt_points[index] for index in indices] for obj, indices in indices_by_object.items()}

    points_by_object_raw = {obj: [points[index] for index in indices] for obj, indices in indices_by_object_raw.items()}
    # Note: The same process is applied to the raw lines as well

    lines = []
    bboxes= []

    # Looping over all objects
    for object_name, points_of_object in points_by_object.items():
        best_bbox = None
        # Process the point cloud data for each object
        if points_of_object:

            # Generate optimal bounding boxes for each object using Open3D and custom functions
            my_pointcloud_for_test = points_by_object[object_name]
            my_pointcloud_for_test_raw = points_by_object_raw[object_name]
            object_point_cloud_raw = np.array(my_pointcloud_for_test_raw)[:, :3] 
            pcd_raw = open3d.geometry.PointCloud()
            pcd_raw.points = open3d.utility.Vector3dVector(object_point_cloud_raw)
            object_point_cloud_fov = np.array(my_pointcloud_for_test)[:, :3] 
            pcd_fov = open3d.geometry.PointCloud()
            pcd_fov.points = open3d.utility.Vector3dVector(object_point_cloud_fov)
            car_df = row.filter(like=object_name)
            best_obb, az_selected = get_optimal_oriented_bounding_box(car_df,extents,object_name,pcd_fov)


            obb =best_obb

            if best_obb is not None:
                points_inside_obb = obb.get_point_indices_within_bounding_box(pcd_fov.points)
                num_points_inside_obb = len(points_inside_obb)
                if num_points_inside_obb != object_point_cloud_fov.shape[0]:
                    obb_expanded = expand_or_adjust_obb(obb, np.array(my_pointcloud_for_test)[:, :3],object_name )
                else:
                    if 'PED' in object_name or 'BIC' in object_name:
                        obb_expanded = expand_or_adjust_obb(obb, np.array(my_pointcloud_for_test)[:, :3],object_name )
                    else:
                        obb_expanded = obb


                best_bbox = np.array([obb_expanded.center[0], obb_expanded.center[1], obb_expanded.center[2], obb_expanded.extent[0], obb_expanded.extent[1], obb_expanded.extent[2], az_selected])
                best_bbox = np.reshape(best_bbox, (1, -1))

                points_inside_raw = obb_expanded.get_point_indices_within_bounding_box(pcd_raw.points)
                num_points_inside_raw = len(points_inside_raw)



                points_inside_fov = obb_expanded.get_point_indices_within_bounding_box(pcd_fov.points)
                num_points_inside_fov = len(points_inside_fov)

                # Calculate the truncation ratio
                if num_points_inside_fov != num_points_inside_raw:
                    truncation = calculate_truncation_ratio(obb_expanded, 1000,V2C_array,R0_array,image_shape, P2_array)
                else:
                    truncation = 0

                Type = None
                if 'CAR' in object_name:
                    Type = 'Car'
                elif 'PED' in object_name:
                    Type = 'Pedestrian'
                elif 'BIC' in object_name:
                    Type = 'Cyclist'
                # Adjust the height of the bounding boxes based on the object type
                if 'CAR' in object_name:
                    best_bbox[0][2] = best_bbox[0][2] - 0.08 
                elif 'PED' in object_name:
                    best_bbox[0][2] = best_bbox[0][2] + 0.02
                elif 'BIC' in object_name:
                    best_bbox[0][2] = best_bbox[0][2] + 0.02
            else:
                print(f"No valid OBB found for object: {object_name}") 
                print(point_cloud_file)
                # Note: If an optimal bounding box can't be generated for an object, set the red_flag to True
                red_flag = True
                
        if best_bbox is not None:
            if all(x is not None for x in best_bbox):
                # Generate labels in KITTI format for each object
                line = generate_kitti_label( best_bbox, P2_array, R0_array, V2C_array, image_shape,truncation, Type)
                lines.append(line)
                bboxes.append(best_bbox)
            else:
                line = ''
                lines.append(line)
                bboxes.append(best_bbox)
        else:
            line = ''
            lines.append(line)
            bboxes.append(best_bbox)
    
    return filt_filt_points, label_file, point_cloud_file, lines, red_flag, bboxes


def save_labels(modified_dir,label_file,lines):
    # Function to save labels into files
    with open(os.path.join(modified_dir, label_file), "w") as f:
        for line in lines:
            f.write(line)

# These are constants used for processing the lidar data and images
POINT_CLOUD_RANGE= [0, -39.68, -3, 69.12, 39.68, 1]
P2_array = np.array([[7.21537720e+02, 0.00000000e+00, 6.09559326e+02, 4.48572807e+01],
[0.00000000e+00, 7.21537720e+02, 1.72854004e+02, 2.16379106e-01],
[0.00000000e+00, 0.00000000e+00, 1.00000000e+00, 2.74588400e-03]], dtype=np.float32)
R0_array = np.array([[ 0.9999239 ,  0.00983776, -0.00744505],
[-0.0098698 ,  0.9999421 , -0.00427846],
[ 0.00740253,  0.00435161,  0.9999631 ]], dtype=np.float32)
V2C_array = np.array([[ 7.53374491e-03, -9.99971390e-01, -6.16602018e-04,-4.06976603e-03],
[ 1.48024904e-02,  7.28073297e-04, -9.99890208e-01, -7.63161778e-02],
[ 9.99862075e-01,  7.52379000e-03,  1.48075502e-02, -2.71780610e-01]], dtype=np.float32)
image_shape = np.array([375, 1242],dtype=np.int32)

# Getting the directory path
folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
subdir_name = os.path.basename(os.path.normpath(sys.argv[1]))
chosen_subdir = os.path.join(folder_path, subdir_name, "lidar")

# Creating the modified directory if it doesn't exist
modified_dir = os.path.join(chosen_subdir, "Modified")
if not os.path.exists(modified_dir):
    os.mkdir(modified_dir)

# Creating the output directory if it doesn't exist
out_dir = os.path.join(modified_dir, "Out")
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

# Reading the 'IDs.txt' file
with open(os.path.join(modified_dir, 'IDs.txt'), 'r') as f:
    data = f.readlines()

# Creating a dictionary of objects with their corresponding numbers
objects = {}
for line in data:
    entity, numbers_str = line.strip().split(": ")
    numbers = [int(n.strip("'[]")) for n in numbers_str.split(", ")]
    objects[entity] = numbers

# Reading the 'Extents.txt' file
with open(os.path.join(modified_dir, 'Extents.txt'), 'r') as f:
    extents = {}
    for line in f:
        fields = line.strip().split()
        entity = fields[0]
        extent_here = [float(x) for x in fields[1:]]
        extents[entity] = extent_here

# Looking for a single .dat file in the chosen directory
dat_files = glob.glob(os.path.join(chosen_subdir, "*.dat"))
if len(dat_files) != 1:
    raise ValueError(f"Expected 1 .dat file in {chosen_subdir}, found {len(dat_files)}")
file_name = dat_files[0]

# Reading the .dat file
length_df=len(extents)*6 +1
df = pd.read_csv(file_name, sep='\t', skiprows=2, usecols=range(1, length_df))
time_carmaker = pd.read_csv(file_name, sep='\t', skiprows=2, usecols=[length_df])

# Naming the columns of the DataFrame
with open(file_name, 'r') as f:
    column_names = f.readline().strip().split('\t')[1:length_df]
df.columns = column_names

# Getting all the .npy files that start with 'lidar' in the directory
files = [file for file in os.listdir(modified_dir) if file.startswith("lidar") and file.endswith("pointcloud.npy")]

# Processing each file one by one
for file in files:
    filt_filt_points, label_file, point_cloud_file, line, red_flag, bboxes =process_pointcloud_data(modified_dir,file,P2_array, R0_array,V2C_array,image_shape,extents,df,time_carmaker)
    if red_flag:
        save_labels(modified_dir,label_file,'')
    else:
        # Comment out the following part if you want to visualize the bounding boxes
        # filtered_bboxes = [bbox for bbox in bboxes if bbox is not None]
        # bbox_array = np.array(filtered_bboxes)
        # bbox_array = np.squeeze(bbox_array)
        # bbox_array = np.reshape (bbox_array, (bbox_array.shape [0], -1))
        # V_mayavi.draw_scenes (points=filt_filt_points, gt_boxes = bbox_array )
        # mlab.show(stop=True)
        save_labels(modified_dir,label_file,line)
