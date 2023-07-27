import shutil
import random
import os 

# Function to count the number of objects in each file
def count_objects(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return len(lines)

# Define various file names and dataset parameters
dataset_name = '....'
labels_avx_kitti_format = 'labels_AVX'
points_AVX_database = 'points_AVX'
calib_avx_kitti_format = 'calib_AVX'
#############################################################################
my_data_size = int(3712*1)  # The size of the data to be used
percent_synthetic = ...  # The proportion of synthetic data to be used
# 0.9 for %90 KITTI %10 AVX training
#############################################################################
kitti_training_train = 'kitti_training_train'  # The directory containing the real training data

# Define the directories for the synthetic data
labels_synthetic = f'data/AVX_DATA/Version_6/Train/{labels_avx_kitti_format}'
points_synthetic = f'data/AVX_DATA/Version_6/Train/{points_AVX_database}'
calib_synthetic = f'data/AVX_DATA/Version_6/Train/{calib_avx_kitti_format}'

# Define the directories for the real data
points_train_real = f'data/{kitti_training_train}'
labels_real = 'data/kitti/training/label_2'
images_real = 'data/kitti/training/image_2'
calib_real = 'data/kitti/training/calib'

# Define the destination directories for the various components of the dataset
points_destination_dir = f'data/{dataset_name}/training/velodyne'
labels_destination_dir = f'data/{dataset_name}/training/label_2'
calib_destination_dir = f'data/{dataset_name}/training/calib'
image_destination_dir = f'data/{dataset_name}/training/image_2'
imagesets = f'data/{dataset_name}/ImageSets'

# Create the destination directories if they do not exist
if not os.path.exists(points_destination_dir):
    os.makedirs(points_destination_dir)
if not os.path.exists(labels_destination_dir):
    os.makedirs(labels_destination_dir)
if not os.path.exists(calib_destination_dir):
    os.makedirs(calib_destination_dir)
if not os.path.exists(image_destination_dir):
    os.makedirs(image_destination_dir)
if not os.path.exists(imagesets):
    os.makedirs(imagesets)

# Get a list of all the label files in the synthetic data directory
label_files_synth = []
for filename in os.listdir(labels_synthetic):
    if filename.endswith('.txt'):
        label_files_synth.append(os.path.join(labels_synthetic, filename))

# Count the number of objects in each synthetic data file
object_counts = {}
for filename in label_files_synth:
    object_counts[filename] = count_objects(filename)

# Sort the synthetic data files based on their object count
sorted_files = sorted(label_files_synth, key=lambda x: object_counts[x], reverse=True)

# Calculate the size of the synthetic data based on the given percentage
synthetic_data_size = int(my_data_size * percent_synthetic)

# Select the synthetic data files up to the calculated size
selected_avx = sorted_files[:synthetic_data_size]

# Convert the synthetic label files to point cloud files
for i in range(len(selected_avx)):
    selected_avx[i] = selected_avx[i].replace(labels_avx_kitti_format, points_AVX_database).replace(".txt", ".npy")

# Get a list of all the point cloud files in the real data directory
files_points_train_real = os.listdir(points_train_real)
files_points_train_real = [f for f in files_points_train_real if f.endswith('.npy')]
files_points_train_real.sort()

# Select the real data files up to the remaining size
files_points_train_real = files_points_train_real[:my_data_size-synthetic_data_size]

# Add the directory path to each real data file
files_points_train_real = [os.path.join(points_train_real, f) for f in files_points_train_real]

# Merge the synthetic and real data lists and shuffle them
train_database = files_points_train_real + selected_avx
random.shuffle(train_database)

# Keep track of existing files to avoid duplication
existing_files = set(os.listdir(points_destination_dir))

new_filenames = []

# Copy and rename each file in the merged list to the destination directory
for i, filename in enumerate(train_database):
    if filename.endswith('.npy'):
        # Define new filenames based on the index
        new_filename = '{:06d}.npy'.format(i)
        while new_filename in existing_files:
            i += 1
            new_filename = '{:06d}.npy'.format(i)
        shutil.copy(filename, os.path.join(points_destination_dir,new_filename))

        # Copy and rename corresponding label, calibration, and image files
        new_label_filename = new_filename.split('.')[0] + '.txt'
        new_image_filename = new_filename.split('.')[0] + '.png'

        # Handle synthetic data
        if points_AVX_database in filename:
            file_name = os.path.basename(filename)
            new_file_name = file_name[:-4] + '.txt'
            new_file_path = filename.replace(points_AVX_database, labels_avx_kitti_format)
            label_AVX_full_path = new_file_path.replace(file_name, new_file_name)
            shutil.copy(label_AVX_full_path, os.path.join(labels_destination_dir,new_label_filename))
            new_file_path_calib = filename.replace(points_AVX_database, calib_avx_kitti_format)
            calib_AVX_full_path = new_file_path_calib.replace(file_name, new_file_name)
            shutil.copy(calib_AVX_full_path, os.path.join(calib_destination_dir,new_label_filename))

        # Handle real data
        if kitti_training_train in filename:
            file_name = os.path.basename(filename)
            file_name = file_name[:-4]
            label_kitti_train_path = os.path.join(labels_real, file_name + '.txt')
            shutil.copy(label_kitti_train_path, os.path.join(labels_destination_dir,new_label_filename))
            calib_kitti_train_path = os.path.join(calib_real, file_name + '.txt')
            shutil.copy(calib_kitti_train_path, os.path.join(calib_destination_dir,new_label_filename))
            image_kitti_train_path = os.path.join(images_real, file_name + '.png')
            shutil.copy(image_kitti_train_path, os.path.join(image_destination_dir,new_image_filename))

        # Add the new filename to the existing files set and new filenames list
        existing_files.add(new_filename)
        new_filenames.append(new_filename.split('.')[0])

# Create a train.txt file with the names of the point cloud files to be used for training
with open(os.path.join(imagesets, 'train.txt'), 'w') as f:
    for filename in new_filenames:
        f.write(filename + '\n')
