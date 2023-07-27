import os
import numpy as np
# This script iterates over each zero row in a point cloud and checks if the corresponding contribution line is not empty.
# This is an error report script. 
# It writes the line number and contribution information to the output file.
# Define the path to the folder containing the subdirectories
folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# List the contents of the parent folder
print("Subdirectories:")
subdirs = []
for name in os.listdir(folder_path):
    # Check if it's a subdirectory
    if os.path.isdir(os.path.join(folder_path, name)):
        print("- " + name)
        subdirs.append(name)

# Ask the user to choose a subdirectory
chosen_subdir = None
while chosen_subdir is None:
    subdir_name = input("Enter the name of a subdirectory to process: ")
    if subdir_name in subdirs:
        chosen_subdir = os.path.join(folder_path, subdir_name, "lidar")
    else:
        print("Invalid subdirectory name.")

# Create a new directory called "Modified" inside chosen_subdir, if it doesn't already exist
modified_dir = os.path.join(chosen_subdir, "Modified")
if not os.path.exists(modified_dir):
    os.mkdir(modified_dir)

# Loop over all the .txt files in the chosen subdirectory
for filename in os.listdir(chosen_subdir):
    if filename.endswith("pointcloud.txt"):
        # Load the .txt file into a Numpy array
        file_path = os.path.join(chosen_subdir, filename)
        data = np.loadtxt(file_path, dtype='float', usecols=(0, 1, 2, 3), skiprows=1)
        contributions_file = filename.replace("pointcloud.txt", "contributions.txt")
        zero_rows = np.where((data[:, 0] == 0) & (data[:, 1] == 0) & (data[:, 2] == 0))[0]  # Find rows containing zeros
        # Create a new file to save the line numbers
        save_file_path = os.path.join(modified_dir, f"{filename}_line_numbers.txt")
        with open(os.path.join(chosen_subdir, contributions_file)) as f:
            lines = f.readlines()  # Read the lines of the contributions file
        with open(save_file_path, "w") as save_file:
            # Loop over each row of the data array
            for i in range(zero_rows.shape[0]):
                # Check if the line corresponding to the zero row is not empty
                if lines[zero_rows[i]] != '\n':
                    # Write the line number and contribution information to the output file
                    save_file.write(f"{zero_rows[i]+1} : {lines[zero_rows[i]]}\n")
