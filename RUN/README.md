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
10. Select OutputQuantities for each Traffic Object (ds.x,y,z :3, r_zyx.x,y,z :3, Time). We used 5 CARs, 2 PEDs, 1 BIC, hence 48 selections + Time at a frequency of 100Hz.

## Run

1. Click the 'Start' button in CarMaker to launch your scenario.
2. Go to the output folder where Ansys AVxcelerate Sensors Simulator's outputs are saved.
3. Copy the CarMaker .DAT file from its saved location to the location where point clouds and contribution outputs are saved.
4. Copy `/Python_scripts` into the same directory where Ansys AVxcelerate Sensors CarMaker Cosimulation's output resides.
5. Open `RunSequenceScripts.py` and define the directories for processing in the `directory_paths` variable.
6. Run the script with the command: `python RunSequenceScripts.py`.

## Investigate Outputs

After running the script, you will find several output files:

- `deleted_files.txt`: Point clouds deleted due to duplication.
- `Extents.txt`: The dimensions - length, width, and height of the traffic objects.
- `IDs.txt`: EntityIDs corresponding to each traffic object.
- `lidar_xxxxx_label.txt`: Label according to KITTI label format.
- `lidar_xxxxx_pointcloud.npy`: Point cloud according to KITTI coordinates.

Check the `Ready` folder for renamed point clouds and their corresponding labels. Please note, this folder only contains the point clouds and labels that successfully captured traffic objects within the field of view.

## Visualize point clouds and 3D bboxes

To visualize the 3D bounding boxes during the generation process, comment out a specific section in the `LidarPointCloudLabelGenerator.py` script.

```python
# Comment out the following part if you want to visualize the bounding boxes
# filtered_bboxes = [bbox for bbox in bboxes if bbox is not None]
# bbox_array = np.array(filtered_bboxes)
# bbox_array = np.squeeze(bbox_array)
# bbox_array = np.reshape (bbox_array, (bbox_array.shape [0], -1))
# V_mayavi.draw_scenes (points=filt_filt_points, gt_boxes = bbox_array )
# mlab.show(stop=True)
```