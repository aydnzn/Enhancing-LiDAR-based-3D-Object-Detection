# Experiments

The experiments designed for this study were grounded on two fundamental principles. First, the weights of the network were initialized randomly to guarantee that no prior knowledge of the data was incorporated. Subsequently, the network structure and parameters are kept consistent across all training and testing stages.

The data sets used in these experiments include both real and synthetic data sets. Further information about these data sets can be found in the Datasets section. For the preparation of training sets, various versions of a preliminary [Python script](../../docs/OrganizeData.py) are utilized.

## Experiment 1: Training on a Single Database

The initial experiment aims to assess the effectiveness of the selected neural network architecture in executing detection tasks. Here, the network is trained exclusively on one data set. Subsequently, the performance of these networks is evaluated on both the KITTI and AVX test sets.

The underlying objective is to understand how robustly the models perform when exposed to diverse data distributions. Real-world data includes a wide array of variability and randomness. In contrast, synthetic data, while containing precise, well-defined features, might lack some of the nuances and unpredictability seen in real-world scenarios.

### Sub-experiment 1: KITTI

- The neural network is trained using real data, followed by validation on both real and synthetic data sets.
- This procedure evaluates the capacity of a model, trained on real-world data, to successfully extrapolate its learned knowledge to synthetic data, and vice versa.

### Sub-experiment 2: AVX

- The neural network is trained solely on synthetic data, followed by validation on both real and synthetic data sets.
- The aim of this approach is to measure the capability of a model, trained on synthetic data, to perform effectively when exposed to real-world data, and vice versa.

## Experiment 2: Training on Combined Databases

The second experiment of this study is formulated to introduce additional variability by merging data from the KITTI and AVX data sets. The objective is to evaluate the capability of combined data sets to augment model performance. This combination leverages the distinctive strengths of both types of data, with real data offering real-world complexity and variability, and synthetic data providing precise, controllable, and plentiful scenarios.

The merged training data set incorporates 3712 frames, aligning with the size of the KITTI training set. This experiment includes several sub-experiments, each utilizing a unique proportion of AVX and KITTI data sets. The overarching aim is to identify an optimal mix of real and synthetic data that boosts model performance across both real and synthetic validation sets.

In each sub-experiment, the total frame count is kept constant at 3712, with the proportion of AVX to KITTI data being varied. For example, in the initial sub-experiment, 90% of the 3712 frames are sourced from the AVX data set, and the remaining 10% from the KITTI data set.

### Sub-experiment 1: 90% AVX, 10% KITTI

- The first sub-experiment involves training the network on a data set composed of 90% AVX data and 10% KITTI data.
- Performance evaluation is undertaken on both KITTI and AVX test sets.

### Sub-experiment 2: 80% AVX, 20% KITTI

- The second sub-experiment involves training the network on a data set composed of 80% AVX data and 20% KITTI data.
- Performance evaluation is undertaken on both KITTI and AVX test sets.

### Sub-experiment 3: 50% AVX, 50% KITTI

- The final sub-experiment utilizes an equal blend of data from both sources, with each contributing 50% of the data set.
- Performance evaluation is undertaken on both KITTI and AVX test sets.

## Experiment 3: Pre-training on Synthetic Data and Fine-Tuning on Real-World Data

The third experiment adopts a fine-tuning approach, wherein the neural network is first pre-trained on synthetic data, followed by subsequent fine-tuning using real-world data. The main aim of this technique is to explore the potential benefits of fine-tuning methods in enhancing neural network performance.

The process begins with the network's pre-training on the AVX data set. Subsequently, fine-tuning is carried out using different portions of the KITTI data set, namely 10%, 20%, and 50% of the total train set.

To assess the impact of synthetic data pre-training, the performance of each fine-tuned model is compared with that of models trained solely on the corresponding subsets of the KITTI data set without pre-training. This comparative analysis aims to shed light on the potential benefits of pre-training on synthetic data for real-world object detection tasks.

### Sub-experiment 1: Fine-Tuning with 10% of KITTI

- In this scenario, the network, initially pre-trained on AVX, is fine-tuned with 10% of the KITTI train set.
- Performance evaluation is undertaken on both KITTI and AVX test sets.
- The performance of this fine-tuned network is compared with a network trained solely on a data set comprising 10% of the KITTI train set.

### Sub-experiment 2: Fine-Tuning with 20% of KITTI

- In this scenario, the network, initially pre-trained on AVX, is fine-tuned with 20% of the KITTI train set.
- Performance evaluation is undertaken on both KITTI and AVX test sets.
- The performance of this fine-tuned network is compared with a network trained solely on a data set comprising 20% of the KITTI train set.

### Sub-experiment 3: Fine-Tuning with 50% of KITTI

- In this scenario, the network, initially pre-trained on AVX, is fine-tuned with 50% of the KITTI train set.
- Performance evaluation is undertaken on both KITTI and AVX test sets.
- The performance of this fine-tuned network is compared with a network trained solely on a data set comprising 50% of the KITTI train set.
