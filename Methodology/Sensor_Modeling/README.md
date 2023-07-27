# Sensor Modeling

This repository provides a comprehensive walkthrough to model the LiDAR sensor for the KITTI dataset, using the Ansys AVxcelerate Sensors Simulator (AVX). The components of the model revolve around a 3D rotating laser scanner, similar to the Velodyne HDL-64E.

## Table of Contents

- [LiDAR Sensor Modeling](#lidar-sensor-modeling)
- [LiDAR Simulation Parameters](#lidar-simulation-parameters)
- [Sensor Layout and Configuration](#sensor-layout-and-configuration)

## LiDAR Sensor Modeling

This section provides a detailed understanding of the creation of a LiDAR sensor model using AVX. Key elements like motion parameters, the Emitter module, the Optics component, the Opto-Electrical module, and the Default Processing module are extensively detailed.

For a deeper understanding of the system’s parametrization and comprehensive overview, navigate to [LiDAR Sensor Modeling readme](./LiDAR_Sensor_Modeling/README.md).

## LiDAR Simulation Parameters

Discover the configuration and layout specifics of the LiDAR sensor, reflecting the setup from the KITTI dataset. Learn how the AVX simulation engine utilizes a JSON parameter file to define critical aspects of the simulation. 

To delve into details about subsampling settings, contribution output, and more, refer to [LiDAR Simulation Parameters readme](./LiDAR_Simulation_Parameters/README.md).

## Sensor Layout and Configuration

Understand how the sensor layout, influenced by the KITTI dataset, impacts the simulation. Despite the change in the vehicle model, find out how the sensor's function of capturing its surroundings remains unaffected.

For more about sensor and vehicle positioning, see [Sensor Layout and Configuration readme](./Sensor_Layout_and_Configuration/README.md).

For a comprehensive understanding of the entire process, please refer to the [full thesis document](../../aydin_uzun_ms_thesis.pdf).
