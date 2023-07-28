import os
import shutil

# Define the source file and directory paths
source_dir = './'
source_file = 'calib_sample.txt'
calib_dir = '...\calib_AVX'
label_dir = '...\labels_AVX'

# Define the parent directory path
parent_dir = '..'

# Define the destination directory path
destination_dir = os.path.join(parent_dir, calib_dir)

# Create the destination directory if it doesn't exist
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# Define the labels directory path
labels_dir = os.path.join(parent_dir, label_dir)

# Iterate over the label files in labels_dir
for label_file in os.listdir(labels_dir):
    if label_file.endswith('.txt'):
        # Generate the destination file path
        destination_file = os.path.join(destination_dir, label_file)

        # Copy the source file to the destination directory with the new name
        shutil.copyfile(os.path.join(source_dir, source_file), destination_file)