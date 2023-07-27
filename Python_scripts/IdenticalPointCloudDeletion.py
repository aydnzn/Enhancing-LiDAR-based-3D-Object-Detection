import os
import filecmp
import sys

# Define paths
folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
subdir_name = os.path.basename(os.path.normpath(sys.argv[1]))
chosen_subdir = os.path.join(folder_path, subdir_name, "lidar")
modified_dir = os.path.join(chosen_subdir, "Modified")

# Create directory if it doesn't exist
if not os.path.exists(modified_dir):
    os.mkdir(modified_dir)

# Function to find identical point cloud files
def find_identical_point_clouds(folder_path):
    # Get all point cloud files
    point_cloud_files = [f for f in os.listdir(folder_path) if f.startswith('lidar') and f.endswith('pointcloud.txt')]
    identical_clouds = []

    # Compare each pair of files
    for i in range(len(point_cloud_files)):
        file1 = point_cloud_files[i]
        for j in range(i + 1, len(point_cloud_files)):
            file2 = point_cloud_files[j]
            # If files are identical, add to the list
            if filecmp.cmp(os.path.join(folder_path, file1), os.path.join(folder_path, file2)):
                identical_clouds.append((file1, file2))

    return identical_clouds

# Function to delete identical point cloud files
def delete_identical_point_clouds(folder_path):
    identical_clouds = find_identical_point_clouds(folder_path)
    deleted_files = []

    # Delete each identical file
    for file1, file2 in identical_clouds:
        file_to_delete = os.path.join(folder_path, file2)
        contribution_file_to_delete = file_to_delete.replace("pointcloud.txt", "contributions.txt")
        # If both files exist, delete them
        if os.path.exists(file_to_delete) and os.path.exists(contribution_file_to_delete):
            os.remove(file_to_delete)
            os.remove(contribution_file_to_delete)
            deleted_files.extend([file_to_delete, contribution_file_to_delete])

    return deleted_files

# Delete identical point clouds
deleted_files = delete_identical_point_clouds(chosen_subdir)

# Create an output file listing the deleted files
output_file_path = os.path.join(modified_dir, "deleted_files.txt")
with open(output_file_path, "w") as output_file:
    output_file.write("\n".join(deleted_files))

# Print out the deleted files and the path to the output file
print("Deleted files:\n", "\n".join(deleted_files))
print("Output file created:", output_file_path)