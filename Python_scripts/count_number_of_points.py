import os
# The script allows the user to choose a specific subdirectory and generates a text file displaying the number of nonzero points.
# Get the absolute path of the parent folder
folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# List the contents of the parent folder
print("Subdirectories:")
subdirs = []
for name in os.listdir(folder_path):
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

output_file = "file.txt"
text_path = os.path.join(chosen_subdir, output_file)

# Create and open the output file
with open(text_path, 'w') as f:
    for filename in os.listdir(chosen_subdir):
        if filename.endswith("pointcloud.txt"):
            point_cloud_file = os.path.join(chosen_subdir, filename)
            point_cloud_name = filename[:-4]
            with open(point_cloud_file, 'r') as pc:
                lines = pc.readlines()
                # Ignore the first entry
                lines = lines[1:]
                # Ignore lines with the first three elements equal to zero
                lines = [line for line in lines if not line.startswith("0 0 0")]
                # Write the point cloud name and the number of nonzero lines to the output file
                f.write(point_cloud_name + " " + str(len(lines)) + "\n")
