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

## OpenPCDet

The [OpenPCDet](https://github.com/open-mmlab/OpenPCDet) platform is utilized for training and evaluation.

Ensure to install OpenPCDet as described in [INSTALL.md](https://github.com/open-mmlab/OpenPCDet/blob/master/docs/INSTALL.md) after fulfilling all requirements.

### Dataset Preparation

#### KITTI Dataset

First, download the official [KITTI 3D object detection](http://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=3d) dataset and organize it as follows:

```
OpenPCDet
├── data
│   ├── kitti
│   │   │── ImageSets
│   │   │── training
│   │   │   ├──calib & velodyne & label_2 & image_2
├── pcdet
├── tools
```

Transfer the [kitti_training_train.7z](https://drive.google.com/file/d/1W0JvxEo4zHE2B_NkSzU7ZCalocEWlVqB/view?usp=share_link) and [kitti_training_val.7z](https://drive.google.com/file/d/1r2a6aX7GURQHm1ydgB1pySmIN3ygmf6p/view?usp=share_link) files to `./OpenPCDet/data` on the VM and extract them. These files are identical to the downloaded KITTI data, but are split into training and validation sets for your convenience.

### Creating Custom Training Sets

For custom training sets, copy the [create_trainset.py](../VM_scripts/create_trainset.py) script to `./OpenPCDet/`. 

Modify parameters like `dataset_name`, `my_data_size`, and `percent_synthtetic` as per your requirements. E.g., if you want a training set with 90% synthetic and 10% KITTI data, set `percent_synthtetic` to 0.9.

The KITTI training data typically contains 3,712 samples. If you wish to create a training set using only a fraction of the KITTI samples, set `percent_synthtetic` to 0 and adjust `my_data_size`. E.g., for a 20% KITTI training set, set `my_data_size` to (3712*0.2).

### Creating Custom Test Sets

For custom test sets, copy the [create_testset_avx.py](../VM_scripts/create_testset_avx.py) and [create_testset_kitti.py](../VM_scripts/create_testset_kitti.py) scripts into `./OpenPCDet/`. Ensure you correctly specify the directory names in the scripts.

Next, move [AVX_testset_KITTI.yaml](../cfgs/AVX_testset_KITTI.yaml) and [KITTI_testset_KITTI.yaml](../cfgs/KITTI_testset_KITTI.yaml) files to `./OpenPCDet/tools/cfgs/dataset_configs/`.

Transfer the [kitti_dataset.py](../VM_scripts/kitti_dataset.py) file to `./OpenPCDet/pcdet/datasets/kitti/`. Make sure to update the `data_path` and `save_path` parameters to match your specific requirements.


For instance, if you want to create a test set with only synthetic samples, set the following values in the `kitti_dataset.py` script:

```python
data_path=ROOT_DIR / 'data' / 'AVX_testset'
save_path=ROOT_DIR / 'data' / 'AVX_testset'
```

Make sure to comment out the sections of the [kitti_dataset.py](../VM_scripts/kitti_dataset.py) related to training, while leaving the testing related sections uncommented:

```python
##################### for TEST
# For Test use this part, for Train comment this part
dataset.set_split(val_split)
kitti_infos_val = dataset.get_infos(num_workers=workers, has_label=True, count_inside_pts=True)
with open(val_filename, 'wb') as f:
    pickle.dump(kitti_infos_val, f)
print('Kitti info val file is saved to %s' % val_filename)
##################### END for TEST
```
Now, run the following commands to create the data info:

```console
python3 -m pcdet.datasets.kitti.kitti_dataset create_kitti_infos tools/cfgs/dataset_configs/ AVX_testset_KITTI.yaml 
```
and
```console
python3 -m pcdet.datasets.kitti.kitti_dataset create_kitti_infos tools/cfgs/dataset_configs/ KITTI_testset_KITTI.yaml 
```
This data info will store necessary parameters, such as bounding box information, for training and evaluation.

For additional details, refer to [GETTING_STARTED.md](https://github.com/open-mmlab/OpenPCDet/blob/master/docs/GETTING_STARTED.md).

## Running the Experiments

### Experiment 1

#### Step 1: Create Trainset for KITTI 

1. Transfer [kitti.yaml](../cfgs/kitti.yaml) to the VM directory `./OpenPCDet/tools/cfgs/dataset_configs/`.

2. Transfer [pointpillar_kitti.yaml](../kitti_models/pointpillar_kitti.yaml) to the VM directory `./OpenPCDet/tools/cfgs/kitti_models/`.

3. Modify the [kitti_dataset.py](../VM_scripts/kitti_dataset.py) file, which is already transferred to `./OpenPCDet/pcdet/datasets/kitti/`. Uncomment the sections related to training and comment the sections related to testing. For instance, uncomment the following block:

    ```python
    ##################### START for TRAIN
    # For Train use this part, for Test comment this part
    dataset.set_split(train_split)
    kitti_infos_train = dataset.get_infos(num_workers=workers, has_label=True, count_inside_pts=True)
    with open(train_filename, 'wb') as f:
        pickle.dump(kitti_infos_train, f)
    print('Kitti info train file is saved to %s' % train_filename)

    print('---------------Start create groundtruth database for data augmentation---------------')
    dataset.set_split(train_split)
    dataset.create_groundtruth_database(train_filename, split=train_split)
    ##################### END for TRAIN
    ```

4. Inside [kitti_dataset.py](../VM_scripts/kitti_dataset.py), adjust the `data_path` and `save_path` parameters according to your specific needs. Make sure to change the values to `kitti`.

#### Step 2: Train KITTI

1. Run the following command to generate the data info needed for training:

    ```console
    python3 -m pcdet.datasets.kitti.kitti_dataset create_kitti_infos tools/cfgs/dataset_configs/kitti.yaml 
    ```

2. Copy [train_modified.py](../VM_scripts/train_modified.py) to `./OpenPCDet/tools/`.

3. Start the training process with this command:

    ```console
    python3 train_modified.py --cfg_file cfgs/kitti_models/pointpillar_kitti.yaml --extra_tag $(if_you_need)$
    ```

#### Step 3: Single epoch Evaluation

For KITTI evaluation, if you only want to evaluate the last epoch, copy the script [test_single_KITTI.py](../VM_scripts/test_single_KITTI.py) to `./OpenPCDet/tools/`. Use the following command to run the evaluation:

```console
python3 test_single_KITTI.py --ckpt [specify_checkpoint_directory] --extra_tag [optional_extra_tag]
```
You should replace `specify_checkpoint_directory` with the directory where your checkpoint is located. Optionally, include the `--extra_tag` parameter if needed.

For AVX evaluation, do the same with [test_single_AVX.py](../VM_scripts/test_multiple_AVX.py).

#### Step 4: Multiple epoch Evaluation

To evaluate multiple epochs selectively, copy the script [select_checkpoints](../VM_scripts/select_checkpoints.py) to `./OpenPCDet/tools/`. This step allows you to choose specific checkpoints for evaluation. If you wish to evaluate all checkpoints, you can skip this step, but note that it may take longer.

Inside [select_checkpoints](../VM_scripts/select_checkpoints.py) you can also modify the following:

```python
    checkpoints_to_copy = [1, 10, 20, 30, 40, 50, 60, 70, 80]
```

to specify the checkpoints you want to copy and then evaluate later. Execute the following command to run the selection process:

```console
python3 select_checkpoints.py [checkpoint_directory]
```

Replace `checkpoint_directory` with the actual path to the directory containing the checkpoints.

For KITTI evaluation with multiple epochs, copy the script [test_multiple_KITTI.py](../VM_scripts/test_multiple_KITTI.py) to `./OpenPCDet/tools/`. Use the following command to perform the evaluation:
 ```console
python3 test_multiple_KITTI.py --ckpt_dir [specify_checkpoints_directory] --extra_tag [optional_extra_tag]
```
Replace `specify_checkpoints_directory` with the actual directory path of the checkpoints. Additionally, include the `--extra_tag` parameter if needed.

Similarly, for AVX evaluation with multiple epochs, copy the script [test_multiple_AVX.py](../VM_scripts/test_multiple_AVX.py) to `./OpenPCDet/tools/`. Use the following command:
```console
python3 test_multiple_AVX.py --ckpt [specify_checkpoints_directory] --extra_tag [optional_extra_tag]
```
Replace `specify_checkpoints_directory` with the actual directory path of the checkpoints. Add the `--extra_tag` parameter if required.

#### Step 5: Visualizing Epoch Evolution with TensorBoard

Once you have the results of your epoch evaluations, you can visualize them with TensorBoard. To do this, follow these steps:

1. Copy the script [tensorboard_visualize.sh](../VM_scripts/tensorboard_visualize.sh) to `./OpenPCDet/`.
2. Modify the `log_dir` parameter in the script to specify the directory containing the log files.
3. Run the script as an executable:
```console
./tensorboard_visualize.sh
```
4. Open your preferred web browser and access the generated TensorBoard visualization.
By executing these steps, you will be able to visualize and analyze the epoch evolution graphs using TensorBoard.

#### Step 6: Train AVX

To create the AVX trainset, follow these steps:

1. Utilize the [create_trainset.py](../VM_scripts/create_trainset.py) script.
2. Modify the `dataset_name` parameter in the script to reflect the desired dataset name.
3. Adjust the `my_data_size` parameter to match the data size of the AVX trainset (your synthetic train set).
4. Set the `percent_synthtetic` parameter to 1 to include only AVX data.
5. Copy [AVX_trainset_KITTI.yaml](../cfgs/AVX_trainset_KITTI.yaml) to `./OpenPCDet/tools/cfgs/dataset_configs/`.
6. Copy [AVX_trainset.yaml](../kitti_models/AVX_trainset.yaml) to `./OpenPCDet/tools/cfgs/kitti_models/`
7. Open the file [kitti_dataset.py](../VM_scripts/kitti_dataset.py) and modify the `data_path` and `save_path` parameters according to your requirements. Again use it in training mode! Ensure that you make the necessary adjustments to the script and configuration files to suit your specific needs.

To generate the required data infos for training, execute the following command:

```console
python3 -m pcdet.datasets.kitti.kitti_dataset create_kitti_infos tools/cfgs/dataset_configs/AVX_trainset_KITTI.yaml
```
You can use the previously copied training script [train_modified.py](../VM_scripts/train_modified.py). Then, run the training using the following command:

```console
python3 train_modified.py --cfg_file cfgs/kitti_models/AVX_trainset.yaml --extra_tag [optional_extra_tag]
```
Replace `optional_extra_tag` with any additional tag if necessary. The evaluation steps will remain the same as described above [Step 3, Step 4, Step 5].

### Experiment 2

For AVX trainsets consisting of 80% AVX and 20% KITTI data, and AVX trainsets with an equal distribution of 50% AVX and 50% KITTI data, the process is straightforward. Now we'll focus on the AVX 90% KITTI 10% case. 

#### AVX 90% KITTI 10%

To create the AVX trainset with a composition of 90% AVX and 10% KITTI data, follow these steps:

1. Utilize the [create_trainset.py](../VM_scripts/create_trainset.py) script.
2. Modify the `dataset_name` parameter in the script to reflect the desired dataset name.
3. Set the `my_data_size` parameter to 3712, which represents the total number of samples in the KITTI train dataset.
4. Adjust the `percent_synthtetic` parameter to 0.9, indicating the desired proportion of AVX data.
5. Copy [AVX_90_kitti_10_train_KITTI.yaml](../cfgs/AVX_90_kitti_10_train_KITTI.yaml) to `./OpenPCDet/tools/cfgs/dataset_configs/`.
6. Copy [AVX_90_kitti_10_train_KITTI.yaml](../kitti_models/AVX_90_kitti_10_train_KITTI.yaml) to `./OpenPCDet/tools/cfgs/kitti_models/`.
7. Open the file [kitti_dataset.py](../VM_scripts/kitti_dataset.py) and modify the `data_path` and `save_path` parameters according to your requirements. Remember to use it in training mode! Ensure that you make the necessary adjustments to the script and configuration files to suit your specific needs.

To generate the required data infos for training, execute the following command:

```console
python3 -m pcdet.datasets.kitti.kitti_dataset create_kitti_infos tools/cfgs/dataset_configs/AVX_90_kitti_10_train_KITTI.yaml
```

You can use the previously copied training script [train_modified.py](../VM_scripts/train_modified.py). Then, run the training using the following command:
```console
python3 train_modified.py --cfg_file cfgs/kitti_models/AVX_90_kitti_10_train_KITTI.yaml --extra_tag [optional_extra_tag]
```
Replace `optional_extra_tag` with any additional tag if necessary. The evaluation steps will remain the same as described above [Step 3, Step 4, Step 5 of Experiment 1].
