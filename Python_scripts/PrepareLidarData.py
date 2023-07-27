import numpy as np  # For numerical operations (not used in the script)
import os  # For operating system dependent functionalities
import shutil  # For high-level file operations
import sys  # To use command line arguments

# Get the absolute path to the parent directory of this script file
folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Get the name of the subdirectory from command line arguments
subdir_name = os.path.basename(os.path.normpath(sys.argv[1]))
# Join the subdirectory name to the parent directory path
chosen_subdir = os.path.join(folder_path, subdir_name, "lidar")

# Create a new directory called "Modified" inside chosen_subdir, if it doesn't already exist
modified_dir = os.path.join(chosen_subdir, "Modified")
if not os.path.exists(modified_dir):
    os.mkdir(modified_dir)

# Define the path to the new directory inside "Modified"
ready_dir = os.path.join(modified_dir, "Ready")

# If 'Ready' directory already exists, delete its contents
if os.path.exists(ready_dir):
    shutil.rmtree(ready_dir)

# Create the 'Ready' directory
os.mkdir(ready_dir)

# Initialize a counter variable
counter = 0

# Loop through the files in the 'Modified' directory
for file in os.listdir(modified_dir):
    # Check if the file is a Lidar point cloud file
    if file.startswith("lidar") and file.endswith("pointcloud.npy"):
        # Store names of associated 'contributions.txt' and 'label.txt' files
        point_cloud_file = file
        label_file = file.replace("pointcloud", "label").replace(".npy", ".txt")
        label_file_path = os.path.join(modified_dir, label_file)

        # Check if the label file exists and is not empty
        if os.path.exists(label_file_path) and os.stat(label_file_path).st_size != 0:
            # Generate new base name for output files
            output_file_base = str(counter).zfill(6)

            # Copy the point cloud and label files to the 'Ready' directory with new names
            shutil.copyfile(os.path.join(modified_dir, point_cloud_file), os.path.join(ready_dir, output_file_base + ".npy"))
            shutil.copyfile(label_file_path, os.path.join(ready_dir, output_file_base + ".txt"))

            # Increment the counter variable
            counter += 1
