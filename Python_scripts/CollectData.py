import os
import shutil
import random
# folders = ['WS03', 'Bridge Concrete AVX','Bridge Steel AVX', 'City AVX','Country AVX', 
#            'Country LHT AVX', 'Country Meander','Country US AVX', 'Highway AVX', 'Highway Japan AVX', 
#            'City AVX v2.2', 'City AVX v3', 'City AVX v4', 'City AVX v5', 'City AVX v6',
#            'MCity Flat AVX v2','City AVX v7','Bridge Steel AVX v2',
#            'Country Meander v2','Country Meander v3','Country Meander v4','Country Meander v5',
#            'Country AVX v2','Country AVX v3','Country AVX v4','Country AVX v5','Country AVX v6', 'Country AVX v7', 'Country AVX v8',
#            'Country AVX v9','Country AVX v10','Country AVX v11','Country AVX v12','Country AVX v13',
#            'Highway AVX v2','Highway AVX v3','Highway AVX v4', 'Highway AVX v5','Highway AVX v6','MCity Flat AVX v3','MCity Flat AVX v4',
#            'MCity Flat AVX v5','MCity Flat AVX v6','MCity Flat AVX v7','MCity Flat AVX v8','MCity Flat AVX v9','MCity Flat AVX v10','MCity Flat AVX v11',
#            'Highway AVX v7','Highway AVX v8','Highway AVX v9','Highway AVX v10',
#            'Bridge Concrete AVX v4','Bridge Concrete AVX v5','Bridge Concrete AVX v6','Bridge Concrete AVX v7','Bridge Concrete AVX v8','Bridge Concrete AVX v9','Bridge Concrete AVX v10',
#            'Country AVX v14','Country AVX v15','Country AVX v16','Country AVX v17','Country AVX v18','Country AVX v19','Country AVX v20']
folders = ['MCity Flat AVX v12', 'MCity Flat AVX v13', 'MCity Flat AVX v14', 'MCity Flat AVX v15', 'MCity Flat AVX v16',
           'MCity Flat AVX v17', 'MCity Flat AVX v18', 'MCity Flat AVX v19', 'MCity Flat AVX v20', 'Highway Japan AVX v2', 'Highway Japan AVX v3',
           'Highway Japan AVX v4', 'Highway Japan AVX v5', 'Highway Japan AVX v6', 'Highway Japan AVX v7','Highway Japan AVX v8',
           'Highway Japan AVX v10','Highway Japan AVX v11','Highway Japan AVX v12','Highway Japan AVX v13','Highway Japan AVX v14',
           'Country AVX v21','Country AVX v22','Country AVX v23','City AVX v8','City AVX v9','City AVX v10','City AVX v11','City AVX v12','City AVX v13','City AVX v14']

src_dir = '..'  # Assuming the script is located in a subfolder of the parent directory
# Destination directories for labels and point cloud data
dst_labels_dir = os.path.join(src_dir, 'AVX_DATA\Version_7\Test\labels')
dst_points_dir = os.path.join(src_dir, 'AVX_DATA\Version_7\Test\points')

# Create the destination directories if they don't exist
if not os.path.exists(dst_labels_dir):
    os.mkdir(dst_labels_dir)

if not os.path.exists(dst_points_dir):
    os.mkdir(dst_points_dir)

# Counter to generate unique filenames
j = 0

# Iterate over each source folder
for folder in folders:
    # Define the path to the 'Ready' subfolder containing the data
    ready_dir = os.path.join(src_dir, folder, 'lidar', 'Modified', 'Ready')

    # Get lists of point cloud and label files
    point_cloud_files = [file for file in os.listdir(ready_dir) if file.endswith('.npy')]
    label_files = [file for file in os.listdir(ready_dir) if file.endswith('.txt')]

    # Randomize the order of point cloud files
    random.shuffle(point_cloud_files)

    # For each point cloud file
    for point_cloud_file in point_cloud_files:
        # Define source paths for the point cloud file and its corresponding label file
        src_point_cloud_path = os.path.join(ready_dir, point_cloud_file)
        src_label_path = os.path.join(ready_dir,  os.path.splitext(point_cloud_file)[0] + '.txt')
        
        # Generate new unique filenames
        j_str = '{:06d}'.format(j)
        new_point_cloud_filename = j_str + '.npy'
        new_label_filename = j_str + '.txt'
        j += 1  # Increment counter
        
        # Define destination paths
        dst_point_cloud_path = os.path.join(dst_points_dir, new_point_cloud_filename)
        dst_label_path = os.path.join(dst_labels_dir, new_label_filename)
        
        # Copy point cloud file and label file to the destination directories
        shutil.copyfile(src_point_cloud_path, dst_point_cloud_path)
        shutil.copyfile(src_label_path, dst_label_path)