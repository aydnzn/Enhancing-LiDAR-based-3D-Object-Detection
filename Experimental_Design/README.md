<!-- # Experimental Design

This part includes the experimental design part of my master thesis.

It includes:
# Data Sets
his project uses the KITTI and AVX data sets for performance evaluation. The KITTI data set contains diverse object classes, including 'Car', 'Pedestrian', 'Cyclist', and others. In contrast, the AVX data set focuses on three distinct classes: 'Car', 'Pedestrian', and 'Cyclist'.

The 'Train' subsets are used for model training, while the 'Test' subsets are used for validation and evaluation.
Dive into [readme](./Datasets/README.md) to understand more.
# Network Settings

This part contains the settings with the [PointPillars Network](https://arxiv.org/abs/1812.05784) for 3D object detection, implemented using the [OpenPCDet](https://github.com/open-mmlab/OpenPCDet) tool. The model targets 'Car', 'Pedestrian', and 'Cyclist' classes.

Training parameters include an 80-epoch duration, Adam optimizer with a learning rate of 0.003, and a batch size of 2. Data preprocessing and augmentation techniques are applied to improve model performance, and post-processing includes non-maximum suppression (NMS).

Dive into [readme](./Network_settings/README.md) to understand more.

# Evaluation Metrics
This part uses KITTI Evaluation Metrics for network assessment, focusing on 'Car', 'Pedestrian', and 'Cyclist' classes. Performance is evaluated using 3D Intersection over Union (IoU) to classify detections as true or false positives. Precision and recall are computed to form a Precision-Recall (PR) curve. Average Precision (AP), derived from the PR curve, is used as the primary performance metric, following the KITTI's 40-Point interpolated AP approach. The Average Orientation Similarity (AOS) metric is also utilized, taking into account object orientation.

Dive into [readme](./Evaluation_metrics/README.md) to understand more.
# Adapting KITTI Difficulty Levels for Synthetic Data Set Evaluation
This part examines the applicability of KITTI difficulty levels ('Easy,' 'Moderate,' 'Hard') to synthetic data sets in the context of object detection. KITTI levels primarily depend on bounding box height, occlusion, and truncation.

For synthetic data evaluation, occlusion is neglected as all objects are considered 'fully visible'. Therefore, difficulty levels for synthetic data solely depend on bounding box height and truncation. Moreover, the 'DontCare' label, significant in real data sets, is omitted in synthetic data evaluation.

Dive into [readme](./Adapting_difficulty/README.md) to understand more.
# Experiments
This part contains a collection of experiments focused on the utilization of neural networks for object detection tasks. The goal is to understand the performance of these networks when trained on both real and synthetic data sets. 

## Experiment 1: Training on a Single Database
This experiment assesses the capability of the neural network architecture when trained exclusively on either the real data set (KITTI) or the synthetic data set (AVX). It aims to determine how the models generalize when faced with different data distributions.

## Experiment 2: Training on Combined Databases
The second experiment evaluates the performance of the model when trained on a combined data set of KITTI and AVX. Different proportions of real and synthetic data are utilized to find the optimal mixture that enhances the model's performance.

## Experiment 3: Pre-training on Synthetic Data and Fine-Tuning on Real-World Data
The third experiment adopts a fine-tuning approach, where the network is first pre-trained on synthetic data (AVX) and then fine-tuned using different portions of the real-world data set (KITTI). The objective is to explore the benefits of fine-tuning methods on enhancing neural network performance.

Dive into [readme](./Experiments/README.md) to understand more.
 -->

# Experimental Design

This repository contains the experimental design of my master's thesis, broken down into these sections:

## Data Sets
I used the KITTI and AVX data sets for performance evaluation, with the 'Train' subsets for model training, and the 'Test' subsets for validation and evaluation. For more details, see the [readme](./Datasets/README.md).

## Network Settings
I used the PointPillars Network for 3D object detection, with the OpenPCDet tool. The model targets 'Car', 'Pedestrian', and 'Cyclist' classes. Training parameters and techniques are also discussed. For more details, see the [readme](./Network_settings/README.md).

## Evaluation Metrics
The KITTI Evaluation Metrics are used for network assessment, which includes the 3D Intersection over Union (IoU), Precision-Recall (PR) curve, Average Precision (AP), and Average Orientation Similarity (AOS) metric. For more details, see the [readme](./Evaluation_metrics/README.md).

## Adapting KITTI Difficulty Levels
I examined the applicability of KITTI difficulty levels to synthetic data sets in object detection context. For more details, see the [readme](./Adapting_difficulty/README.md).

## Experiments
A collection of experiments are included, which focus on neural network performance when trained on both real and synthetic data sets. For more details, see the [readme](./Experiments/README.md).
