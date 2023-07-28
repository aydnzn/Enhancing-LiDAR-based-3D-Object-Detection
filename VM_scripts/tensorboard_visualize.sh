#!/bin/bash

log_dir="/home/auzun/Documents/OpenPCDet/output/kitti_models/................................../tensorboard_val"
# Variable 'log_dir' storing the path to the log directory

cd "$log_dir" || exit  # Change the current directory to 'log_dir' or exit if the directory does not exist

tensorboard --logdir=.  # Run TensorBoard with the current directory as the log directory
