import argparse
from tools.visual_utils import open3d_vis_utils as V
import numpy as np
import os

parser = argparse.ArgumentParser(description='Visualize point cloud scenes')
parser.add_argument('--object_class', type=str, choices=['Car', 'Pedestrian', 'Cyclist'], help='Specify the class to filter filenames')
parser.add_argument('--folder_path', type=str, help='Specify the path to the folder containing the files')

args = parser.parse_args()

selected_class = args.object_class
folder_path = args.folder_path

# Get a list of filenames in the folder_path and sort them in ascending order
filenames = sorted([filename for filename in os.listdir(folder_path) if filename.endswith('bin')])

for filename in filenames:  # Iterate over each filename
    if selected_class in filename:  # Check if the selected class is present in the filename
        file_path = os.path.join(folder_path, filename)  # Construct the file path

        points = np.fromfile(file_path, dtype=np.float32).reshape(-1, 4)  # Load point cloud data from file
        print(filename)  # Print the filename
        V.draw_scenes(points=points)  # Visualize the point cloud scenes
