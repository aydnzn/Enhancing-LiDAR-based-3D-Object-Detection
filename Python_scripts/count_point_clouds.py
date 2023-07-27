import os
#The script counts the number of point cloud files in each specified directory and provides the overall count at the end.
# List of directory paths
directory_paths = ['WS03', 'Bridge Concrete AVX', 'Bridge Steel AVX', 'City AVX', 'Country AVX', 
                   'Country LHT AVX', 'Country Meander', 'Country US AVX', 'Highway AVX', 'Highway Japan AVX', 
                   'City AVX v2.2', 'City AVX v3', 'City AVX v4', 'City AVX v5', 'City AVX v6',
                   'MCity Flat AVX v2', 'City AVX v7', 'Bridge Steel AVX v2',
                   'Country Meander v2', 'Country Meander v3', 'Country Meander v4', 'Country Meander v5',
                   'Country AVX v2', 'Country AVX v3', 'Country AVX v4', 'Country AVX v5', 'Country AVX v6', 'Country AVX v7', 'Country AVX v8',
                   'Country AVX v9', 'Country AVX v10', 'Country AVX v11', 'Country AVX v12', 'Country AVX v13',
                   'Highway AVX v2', 'Highway AVX v3', 'Highway AVX v4', 'Highway AVX v5', 'Highway AVX v6', 'MCity Flat AVX v3', 'MCity Flat AVX v4',
                   'MCity Flat AVX v5', 'MCity Flat AVX v6', 'MCity Flat AVX v7', 'MCity Flat AVX v8', 'MCity Flat AVX v9', 'MCity Flat AVX v10', 'MCity Flat AVX v11',
                   'Highway AVX v7', 'Highway AVX v8', 'Highway AVX v9', 'Highway AVX v10',
                   'Bridge Concrete AVX v4', 'Bridge Concrete AVX v5', 'Bridge Concrete AVX v6', 'Bridge Concrete AVX v7', 'Bridge Concrete AVX v8', 'Bridge Concrete AVX v9', 'Bridge Concrete AVX v10',
                   'Country AVX v14', 'Country AVX v15', 'Country AVX v16', 'Country AVX v17', 'Country AVX v18', 'Country AVX v19', 'Country AVX v20']

total_directories = len(directory_paths)
total_point_clouds = 0

# Iterate over the directory paths
for directory_path in directory_paths:
    # Get the absolute path of the parent folder
    folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    subdir_name = directory_path
    chosen_subdir = os.path.join(folder_path, subdir_name, "lidar")
    modified_dir = os.path.join(chosen_subdir, "Modified")

    # Retrieve the point cloud files starting with 'lidar_' and ending with 'pointcloud.npy'
    point_cloud_files = [file for file in os.listdir(modified_dir) if file.startswith('lidar_') and file.endswith('pointcloud.npy')]
    total_point_clouds += len(point_cloud_files)

# Print the total number of directory paths and point clouds
print(f"Total number of directory paths: {total_directories}")
print(f"Total number of point clouds: {total_point_clouds}")
