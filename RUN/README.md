# How to Run

Follow the steps below to setup, run, and analyze your scenario:

## Setup

1. Set up the AVXConnector in CarMaker.
2. Set up the Object Sensor in CarMaker.
3. Create routes for Traffic Objects via Scenario Editor.
4. Create Traffic Objects and name them (e.g., 'CAR1', 'CAR2', 'BIC1', 'PED1').
5. Select 'Movie Geometry' for each Traffic Object.
6. Add a route and set a start position for each Traffic Object.
7. Set a motion model and maneuver for each Traffic Object.
8. For optimal performance, limit traffic objects to a maximum of 7-8 to avoid memory errors. 
9. Create a maneuver for EGO car.
10. Select OutputQuantities for each Traffic Object (ds.x,y,z :3, r_zyx.x,y,z :3, Time). E.g. if you used 5 CARs, 2 PEDs, 1 BIC, hence 48 selections + Time at a frequency of 100Hz.

## Run

1. Click the 'Start' button in CarMaker to launch your scenario.
2. Go to the output folder where Ansys AVxcelerate Sensors Simulator's outputs are saved.
3. Copy the CarMaker .DAT file from its saved location to the location where point clouds and contribution outputs are saved.
4. Copy `/Python_scripts` into the same directory where Ansys AVxcelerate Sensors CarMaker Cosimulation's output resides.
5. Open `RunSequenceScripts.py` and define the directories for processing in the `directory_paths` variable.
6. Run the script with the command: `python RunSequenceScripts.py`.

## Investigate Outputs

After running the script, you will notice there are several output files:

- `deleted_files.txt`: Point clouds deleted due to duplication. See [README.md](../Methodology/Processing/README.md).
- `Extents.txt`: The dimensions - length, width, and height of the traffic objects. See [README.md](../Methodology/Processing/README.md).
- `IDs.txt`: EntityIDs corresponding to each traffic object. See [README.md](../Methodology/Processing/README.md).
- `lidar_xxxxx_label.txt`: Label according to KITTI label format. See [README.md](../Methodology/Processing/README.md).
- `lidar_xxxxx_pointcloud.npy`: Point cloud according to KITTI coordinates. See [README.md](../Methodology/Processing/README.md).

Check the `Ready` folder for renamed point clouds and their corresponding labels. Please note, this folder only contains the point clouds and labels that successfully captured traffic objects within the field of view.

## Visualize point clouds and 3D bboxes

To visualize the 3D bounding boxes during the label generation process, comment out a specific section in the `LidarPointCloudLabelGenerator.py` script.

```python
# Comment out the following part if you want to visualize the bounding boxes
# filtered_bboxes = [bbox for bbox in bboxes if bbox is not None]
# bbox_array = np.array(filtered_bboxes)
# bbox_array = np.squeeze(bbox_array)
# bbox_array = np.reshape (bbox_array, (bbox_array.shape [0], -1))
# V_mayavi.draw_scenes (points=filt_filt_points, gt_boxes = bbox_array )
# mlab.show(stop=True)
```
## Scaling Up

To create a larger synthetic point cloud database with KITTI-like labels, you can create additional routes and scenarios. For details, see [Scaling_Simulated_Scenarios](../Methodology/Scaling_Simulated_Scenarios/README.md). In my research, I used the CarMaker Co-simulation Library to simulate driving scenarios in various virtual environments, generating a significant number of useful point cloud frames.

You can define multiple directories for processing in the `directory_paths` variable in [RunSequenceScripts.py](../Python_scripts/RunSequenceScripts.py).

Please note that only the data inside the `Ready` folder will be utilized in further processing. You may delete intermediate outputs to conserve storage space.

## Collecting Data

Use the [CollectData.py](../Python_scripts/CollectData.py) script to assemble your dataset from your own unique scenarios. Ensure to modify variables such as `dst_labels_dir` and `dst_points_dir`, and `folders` to match your requirements.

## Calibration

Deploy the [CalibGenerator.py](../Python_scripts/CalibGenerator.py) script to duplicate the constant calibration parameter used for every frame during training and evaluation. Modify `calib_dir` and `label_dir` inside `CalibGenerator.py` as needed.

With these steps, your training and evaluation sets are now ready.

## Hardware and Software Requirements

The experiments in my study were performed on a high-performance computing infrastructure, specifically an Intel(R) Xeon(R) Gold 6238R CPU running at 2.20 GHz with 32 cores, and a RTX8000P-8Q virtual GPU with a total memory of 8192MB.

The datasets were transferred to a Virtual Machine (VM) using WinSCP, stored in the following folders:

```
Train
├── point_AVX : This contains synthetic point cloud data files in .npy format.
├── labels_AVX : This contains the corresponding labels for the point cloud frames. These labels, provided in KITTI format.
├── calib_AVX : This contains the corresponding calibration parameters for the point cloud frames, also in KITTI format.

```

```
Test
├── point_AVX : This contains synthetic point cloud data files in .npy format.
├── labels_AVX : This contains the corresponding labels for the point cloud frames. These labels, provided in KITTI format.
├── calib_AVX : This contains the corresponding calibration parameters for the point cloud frames, also in KITTI format.
```


The experiments were conducted using Python 3.10.6, compiled with GCC 11.3.0. Training and testing of the models were carried out using PyTorch version 1.13.1+cu117, with support from NVIDIA's CUDA toolkit (version 11.7) for GPU-accelerated operations.

## Training and Evaluation

For the training and evaluation stages, the [OpenPCDet](https://github.com/open-mmlab/OpenPCDet) platform will be used.

