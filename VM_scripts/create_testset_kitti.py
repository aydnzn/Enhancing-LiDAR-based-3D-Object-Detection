import os
import shutil

# Set directory and file paths
dataset_name = 'KITTI_testset'
points_AVX_database = 'kitti_training_val'

points_synthetic = f'data/{points_AVX_database}'
labels_synthetic = 'data/kitti/training/label_2'
images_real = 'data/kitti/training/image_2'
calib_synthetic = 'data/kitti/training/calib'

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

# Copy real point clouds to points_destination_dir
for filename in os.listdir(points_synthetic):
    if filename.endswith('.npy'):
        shutil.copy(os.path.join(points_synthetic, filename), points_destination_dir)

# Create val.txt file with point cloud filenames
with open(os.path.join(imagesets, 'val.txt'), 'w') as f:
    files = os.listdir(points_destination_dir)
    files = sorted([f for f in files if f.endswith('.npy')])  # Sort and filter files
    for i, filename in enumerate(files):
        f.write(filename.split('.')[0])
        if i != len(files) - 1:
            f.write('\n')

# Copy real label files to labels_destination_dir
# Read the contents of val.txt into a variable
with open(os.path.join(imagesets, 'val.txt'), 'r') as f:
    val_contents = f.read()

# Copy real label files to labels_destination_dir
for filename in os.listdir(labels_synthetic):
    if filename.endswith('.txt') and filename.split('.')[0] in val_contents:
        shutil.copy(os.path.join(labels_synthetic, filename), labels_destination_dir)

# Copy real label files to labels_destination_dir
for filename in os.listdir(calib_synthetic):
    if filename.endswith('.txt') and filename.split('.')[0] in val_contents:
        shutil.copy(os.path.join(calib_synthetic, filename), calib_destination_dir)

# Copy real label files to labels_destination_dir
for filename in os.listdir(images_real):
    if filename.endswith('.png') and filename.split('.')[0] in val_contents:
        shutil.copy(os.path.join(images_real, filename), image_destination_dir)
