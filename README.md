# Enhancing LiDAR-based 3D Object Detection through Simulation

This repository is dedicated to the Master's Thesis in Electrical Engineering and Information Technology at the [Institute for Measurement Systems and Sensor Technology, Technische Universität München](https://www.ee.cit.tum.de/en/mst/home/).

- Author: [Aydin Uzun](https://www.linkedin.com/in/aydin-uzun-19455679/)
- Contributor: [M.Eng. Arsalan Haider](https://campus.tum.de/tumonline/visitenkarte.show_vcard?pPersonenId=A0E4CB5D125483F9&pPersonenGruppe=3)
- Assessor: [Prof. Dr.-Ing. habil. Dr. h.c. Alexander W. Koch](https://www.ee.cit.tum.de/mst/team/professor-dr-ing-a-w-koch/)
- External Supervisors: [Dr. Petr Fomin](https://www.linkedin.com/in/dr-petr-fomin/), [Günther Hasna](https://www.linkedin.com/in/gfphasna/?originalSubdomain=de)
- Company: [Ansys Germany GmbH](https://www.linkedin.com/company/ansys-inc/)
- Submission Date: 20.06.2023

This Master's thesis investigates the enhancement of LiDAR-based 3D Object Detection algorithms for autonomous vehicles, using synthetic point cloud data generated from the Ansys AVxcelerate CarMaker Co-Simulation process. The study focuses on integrating and aligning synthetic and real-world data, and applying fine-tuning techniques within the Pointpillars network to optimize the model. The research reveals challenges in ensuring model generalization across different data types, especially when identifying complex entities like pedestrians. The study indicates that a balanced combination of synthetic and real-world data yields promising results. Additionally, a hybrid training approach, consisting of initial pre-training with synthetic data followed by fine-tuning with real-world data, exhibits potential, particularly under conditions of real-world data scarcity. This study thus provides valuable insights to guide future improvements in the training and testing methodologies for autonomous driving systems.


## Problem Statement

Despite the accuracy of depth perception provided by LiDAR technology, training deep learning algorithms for LiDAR-based object detection poses a significant challenge due to the scarcity of large-scale annotated data.

Synthetic data generation through simulation software is a potential solution, but often fails to accurately mimic real-world sensory data due to a reliance on handcrafted 3D assets and simplified physics, creating a 'synthetic-to-real gap'. Furthermore, models trained solely on synthetic data may not perform well in real-world scenarios due to data distribution differences.

As part of this research, I'll be investigating how to bridge this gap using the Ansys AVxcelerate Sensors Simulator (AVX). AVX offers a virtual testing environment for sensors used in autonomous vehicles, potentially helping bridge the synthetic-to-real gap. However, the accuracy of this simulator in replicating real-world data and its impact on the performance of algorithms needs to be critically evaluated.

## Objectives

The main objectives are outlined below.

- Generate a replica of the renowned [KITTI](https://www.cvlibs.net/datasets/kitti/) dataset using synthetic data from the [Velodyne HDL-64E LiDAR](https://velodynelidar.com/blog/hdl-64e-lidar-sensor-retires/) model in [Ansys AVxcelerate Sensors Simulator (AVX)](https://www.ansys.com/products/av-simulation/ansys-avxcelerate-sensors), in co-simulation with [CarMaker](https://ipg-automotive.com/en/products-solutions/software/carmaker/) software.
- Apply bounding box extraction algorithms to synthetic point clouds and create KITTI-compatible labels.
- Investigate the potential of synthetic data in enhancing the performance of object detection algorithms.
- Compare performance metrics of models trained on diverse data types (synthetic versus real-world).
- Evaluate the influence of modifying the ratio of synthetic to real-world data on the performance.
- Assess the viability and efficacy of a hybrid training strategy involving pre-training on synthetic data with subsequent fine-tuning on real-world data.
- Analyze the impact of pre-training duration on the optimization of model parameters.
- Conduct a detailed qualitative analysis of the trained networks.

Through these objectives, I aim to provide valuable insights into the benefits and challenges of using synthetic data in training object detection algorithms for autonomous vehicles. 

## Contents:

[Thesis](aydin_uzun_ms_thesis.pdf): This is my master thesis pdf document.
[Methodology](/Methodology/): In this part, the research methodology is outlined. Emphasis is placed on the modeling of the LiDAR sensor. It offers a detailed account of the Ansys AVxcelerate CarMaker Co-Simulation process, elaborates on the processing of simulation outputs, and outlines how simulated scenarios are scaled.
[Experimental_Design](/Experimental_Design/): The part describes the experimental design. It specifies the data sets used, explains the settings of the network, the evaluation metrics, and how KITTI difficulty levels are adapted for synthetic data set evaluation. It also presents the different experiments carried out.
[Results](/Results/): This part delves into the results from the experiments. A quantitative analysis of the results from each experiment is provided, along with an impact assessment of pre-training and training duration on the Average Precision for 3D object detection (AP 3D) scores. A qualitative analysis on the AVX test set and KITTI test set is also included.
[Python_scripts](/Python_scripts/):
[VM_scripts](/VM_scripts/):
[cfgs](/cfgs/):
[kitti_models](/kitti_models/) : 
[docs](/docs/):
[RUN](/RUN/):



