# Network Settings

The [PointPillars Network](https://arxiv.org/abs/1812.05784), known for its unique and beneficial design, was chosen as the main architecture for this study. Characterized by the exclusive use of 2D convolutional layers, it offers an efficient way to manage LiDAR point cloud data. This architecture's effectiveness, performance, and simplicity made the PointPillars Network a suitable choice for experiments with both real and synthetic data.

The experiments in this study were performed using high-performance computing infrastructure. The hardware included a server-grade Intel(R) Xeon(R) Gold 6238R CPU running at 2.20 GHz with 32 cores, complemented by a powerful RTX8000P-8Q virtual GPU with a total memory of 8192MB.

In terms of software, the experiments were conducted using Python 3.10.6, compiled with GCC 11.3.0. The models' training and testing leveraged PyTorch, version 1.13.1+cu117. NVIDIA's CUDA toolkit (version 11.7) was installed to support GPU-accelerated operations in PyTorch.

[OpenPCDet](https://github.com/open-mmlab/OpenPCDet) was chosen as the main tool for the PointPillars network's implementation in this study. OpenPCDet is a robust, open-source PyTorch-based codebase specifically designed for 3D object detection in point cloud data.

OpenPCDet was used in this study with its default training configurations for the PointPillars model. 

The experiments focus on detecting three object classes: 'Car', 'Pedestrian', and 'Cyclist', using the PointPillars model. This model was used consistently across all experiments. The detailed configuration is provided in the [script](../../docs/config.yml).

Data preprocessing involves several steps, including masking points and boxes outside a predefined range, shuffling points during training to improve model generalization, and transforming points into voxels.

The range for the point cloud, specified in meters, is as follows:

- xmin ymin zmin xmax ymax zmax: [0, -39.68, -3, 69.12, 39.68, 1]

The canvas size is computed by finding the range difference in each dimension (xmax - xmin for the x-axis and ymax - ymin for the y-axis) and dividing it by the grid resolution of 0.16 meters. This results in a canvas size of 432 x 496.

During training, the maximum number of points per voxel is limited to 100, and the total number of voxels is restricted to 12,000. This generates a dense tensor of dimensions (D = 9, P = 12000, N = 100), where D represents the dimensionality of the augmented lidar points. A detailed explanation of these parameters can be found in the corresponding section.

Each point undergoes a linear layer operation, followed by batch normalization and ReLU, resulting in a tensor of dimensions (C = 64, P= 12000, N=100). Here, C represents the number of output features of the encoder network. The max operation across pillars yields an output tensor of dimensions (C=64, P = 12000). After redistributing P pillars back to their original locations, a pseudo-image of dimensions (C = 64, H = 432, W = 496) is created. This 3D tensor of size 64 x 432 x 496 serves as input to the backbone. A visual representation of this process is provided in the [original work](https://arxiv.org/abs/1812.05784).

The backbone, the network's feature extraction part, comprises three blocks: Block1(S = 2, L = 4, C = 64), Block2(2S = 4, L = 6, 2C = 128), and Block3(4S = 8, L = 6, 4C = 256). Details on these blocks can be found in the [original work](https://arxiv.org/abs/1812.05784). The backbone sequentially processes the data, progressively increasing the number of 2D convolution filters to learn complex features as the spatial dimension reduces.

The process is followed by an upsampling stage that includes: Up1(Sin=2, Sout=2, 2C=128), Up2(Sin=4, Sout=2, 2C=128) and Up3(Sin=8, Sout=2, 2C=128). These deconvolution blocks aim to upsample the features back to their original resolution. See [original work](https://arxiv.org/abs/1812.05784).

The features of Up1, Up2, and Up3 are then concatenated, providing 6C = 384 features for the detection head. A visual representation of this process is provided in the [original work](https://arxiv.org/abs/1812.05784).

Subsequently, the detection segment uses a dense layer, which leverages high-level features extracted from the backbone. The anchor-based detection head is designed to form unique sets of anchors for each class.

Training lasts for 80 epochs and utilizes the Adam optimizer with a learning rate of 0.003 and a batch size of 2. The loss function employed is a weighted sum of classification, localization, and direction classification losses.

Post-processing of the model's output includes non-maximum suppression (NMS). Instead of pre-training, weights are randomly initialized through a uniform distribution. A fixed random seed is used to ensure reproducibility and consistency of results across different runs.

Lastly, data augmentation is used to increase the diversity of the training set. This process introduces random but realistic transformations to the data, such as rotations and flips. The augmentation pipeline also includes ground truth sampling, random world flipping along the x-axis, random rotation within a predefined range, and random scaling.

The training process was carried out using a modified version of the training script derived from the OpenPCDet framework.

