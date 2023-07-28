import os
import shutil
import random

def count_objects(filename):
    # Counts the number of lines in a file
    with open(filename, 'r') as f:
        lines = f.readlines()
    return len(lines)

# Set directory and file paths
dataset_name = 'AVX_90_kitti_10_train_KITTI'
labels_avx_kitti_format = 'labels_AVX'
points_AVX_database = 'points_AVX'
calib_avx_kitti_format = 'calib_AVX'
my_data_size = int(3712*1)
percent_synthetic = 0.9
kitti_training_train = 'kitti_training_train'

labels_synthetic = f'data/AVX_DATA/Version_6/Train/{labels_avx_kitti_format}'
points_synthetic = f'data/AVX_DATA/Version_6/Train/{points_AVX_database}'
calib_synthetic = f'data/AVX_DATA/Version_6/Train/{calib_avx_kitti_format}'

points_train_real = f'data/{kitti_training_train}'
labels_real = 'data/kitti/training/label_2'
images_real = 'data/kitti/training/image_2'
calib_real = 'data/kitti/training/calib'

points_destination_dir = f'data/{dataset_name}/training/velodyne'
labels_destination_dir = f'data/{dataset_name}/training/label_2'
calib_destination_dir = f'data/{dataset_name}/training/calib'
image_destination_dir = f'data/{dataset_name}/training/image_2'
imagesets = f'data/{dataset_name}/ImageSets'

# Create imagesets directory if it does not exist
if not os.path.exists(points_destination_dir):
    os.makedirs(points_destination_dir)

if not os.path.exists(labels_destination_dir):
    os.makedirs(labels_destination_dir)

if not os.path.exists(calib_destination_dir):
    os.makedirs(calib_destination_dir)

if not os.path.exists(image_destination_dir):
    os.makedirs(image_destination_dir)

# Create imagesets directory if it does not exist
if not os.path.exists(imagesets):
    os.makedirs(imagesets)

# Get a list of all the label files in the synthetic dataset directory
label_files_synth = []
for filename in os.listdir(labels_synthetic):
    if filename.endswith('.txt'):
        label_files_synth.append(os.path.join(labels_synthetic, filename))

# Count the number of objects in each label file and store the counts in a dictionary
object_counts = {}
for filename in label_files_synth:
    object_counts[filename] = count_objects(filename)

# Sort the label files based on their object count in descending order
sorted_files = sorted(label_files_synth, key=lambda x: object_counts[x], reverse=True)

# Calculate the size of the synthetic data based on the desired data size and percentage
synthetic_data_size = int(my_data_size * percent_synthetic)

# Select the top synthetic_data_size files from the sorted list of label files
selected_avx = sorted_files[:synthetic_data_size]

# Modify the selected label file paths to match the corresponding point cloud file paths
for i in range(len(selected_avx)):
    selected_avx[i] = selected_avx[i].replace(labels_avx_kitti_format, points_AVX_database).replace(".txt", ".npy")

# Get a list of all the point cloud files in the real dataset directory
files_points_train_real = os.listdir(points_train_real)

# Filter and sort the point cloud files
files_points_train_real = [f for f in files_points_train_real if f.endswith('.npy')]
files_points_train_real.sort()

# Select a subset of point cloud files based on the remaining data size after adding synthetic data
files_points_train_real = files_points_train_real[:my_data_size - synthetic_data_size]

# Add the directory path to each file name in the list
files_points_train_real = [os.path.join(points_train_real, f) for f in files_points_train_real]

# Merge the point cloud files from the real and synthetic datasets and shuffle the merged list
train_database = files_points_train_real + selected_avx
random.shuffle(train_database)

# Create a set of existing files in the destination directory
existing_files = set(os.listdir(points_destination_dir))

new_filenames = []

# Copy and rename the point cloud files to the destination directory, and also copy and rename the corresponding label and calibration files
for i, filename in enumerate(train_database):
    if filename.endswith('.npy'):
        train_point_cloud_name = os.path.basename(filename)
        new_filename = '{:06d}.npy'.format(i)
        
        # Check if the new filename already exists in the destination directory
        while new_filename in existing_files:
            i += 1
            new_filename = '{:06d}.npy'.format(i)
        
        # Copy the point cloud file
        shutil.copy(filename, os.path.join(points_destination_dir, new_filename))
        
        # Copy and rename the label file
        new_label_filename = new_filename.split('.')[0] + '.txt'
        new_image_filename = new_filename.split('.')[0] + '.png'
        
        if points_AVX_database in filename:
            # Copy and rename the label and calibration files for the synthetic dataset
            file_name = os.path.basename(filename)
            new_file_name = file_name[:-4] + '.txt'
            new_file_path = filename.replace(points_AVX_database, labels_avx_kitti_format)
            label_AVX_full_path = new_file_path.replace(file_name, new_file_name)
            shutil.copy(label_AVX_full_path, os.path.join(labels_destination_dir, new_label_filename))
            new_file_path_calib = filename.replace(points_AVX_database, calib_avx_kitti_format)
            calib_AVX_full_path = new_file_path_calib.replace(file_name, new_file_name)
            shutil.copy(calib_AVX_full_path, os.path.join(calib_destination_dir, new_label_filename))

        if kitti_training_train in filename:
            # Copy and rename the label, calibration, and image files for the real dataset
            file_name = os.path.basename(filename)
            file_name = file_name[:-4]
            label_kitti_train_path = os.path.join(labels_real, file_name + '.txt')
            shutil.copy(label_kitti_train_path, os.path.join(labels_destination_dir, new_label_filename))

            calib_kitti_train_path = os.path.join(calib_real, file_name + '.txt')
            shutil.copy(calib_kitti_train_path, os.path.join(calib_destination_dir, new_label_filename))
            image_kitti_train_path = os.path.join(images_real, file_name + '.png')
            shutil.copy(image_kitti_train_path, os.path.join(image_destination_dir, new_image_filename))

        existing_files.add(new_filename)
        new_filenames.append(new_filename.split('.')[0])

# Create a train.txt file with the point cloud filenames
with open(os.path.join(imagesets, 'train.txt'), 'w') as f:
    for filename in new_filenames:
        f.write(filename + '\n')
