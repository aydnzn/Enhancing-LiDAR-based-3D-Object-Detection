import os
import numpy as np
import sys

# Define the absolute path to the parent folder
folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Extract the name of the subdirectory from the script argument
subdir_name = os.path.basename(os.path.normpath(sys.argv[1]))
# Form the full path to the chosen subdirectory
chosen_subdir = os.path.join(folder_path, subdir_name, "lidar")

# Create a new directory named "Modified" inside chosen_subdir, if it doesn't exist yet
modified_dir = os.path.join(chosen_subdir, "Modified")
if not os.path.exists(modified_dir):
    os.mkdir(modified_dir)

# Loop over all .txt files in the chosen subdirectory
for filename in os.listdir(chosen_subdir):
    if filename.endswith("pointcloud.txt"):
        # Load the .txt file into a Numpy array
        file_path = os.path.join(chosen_subdir, filename)
        # Load data from columns (0, 1, 2, 3), skipping the first row
        data = np.loadtxt(file_path, dtype='float', usecols=(0, 1, 2, 3), skiprows=1)
        # Swap columns 0 and 2, and 1 and 0 to achieve the required transformation
        data[:, [0, 1, 2]] = data[:, [2, 0, 1]]
        # Save the transformed Numpy array as a .npy file in the "Modified" directory
        npy_filename = os.path.splitext(filename)[0] + '.npy'
        np.save(os.path.join(modified_dir, npy_filename), data)

# Print a success message
print("Conversion complete!")