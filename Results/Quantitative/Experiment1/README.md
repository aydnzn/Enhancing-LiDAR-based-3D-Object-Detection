# Results from Experiment 1

<figure>
  <img src="../figs/table_1.png" alt="">
  <figcaption></figcaption>
</figure>

The table presents the AP performance results of the first experiment, which involved object detection tasks for vehicles (CAR), pedestrians (PEDESTRIAN), and cyclists (CYCLIST), using diverse data sets for training and testing -- the KITTI and AVX sets.

Four evaluation metrics are employed in this experiment: AP\_2D, AP\_3D, AP\_BEV, and AOS. In the table, these metrics are represented as **Bbox** for AP\_2D, **3d** for AP\_3D, **bev** for AP\_BEV, and **aos** for AOS. 

The 'Training duration' column represents the duration of the model's training phase, performed with a batch size of 2 and epoch size of 80. The 'Train' and 'Test' columns indicate the data sets employed for training and testing the model, respectively. The subsequent columns report the AP values for different evaluation metrics across the three object categories.

High scores are represented in green color, while low scores are indicated in red in the table.

The first row of the table shows the performance of a model that has been trained and tested on the real-world data set, KITTI. Across all metrics and object categories, this model reports high AP values.

The second row shows that a model trained on KITTI struggles when tested on synthetic AVX data, especially with complex subjects like pedestrians. 

In the third row, a model trained on synthetic AVX underperforms when tested on the real-world KITTI data set. This emphasizes the need for a strategic combination of synthetic and real-world data to develop robust models. 

Lastly, the fourth row demonstrates that a model trained and tested on the synthetic AVX data set performs exceptionally well.

Pedestrian detection poses unique challenges, including smaller image size and the likelihood of occlusion, which can result in low cross-validation scores when synthetic and real-world data have significant differences. 

Moreover, disparities in object distribution across training sets could lead to biased learning, resulting in over-prediction of objects more frequently seen in training data.

The varying performance of models trained and tested on different data sets highlights the inherent differences between synthetic and real-world data. Real-world data encapsulates more complexity and variability, potentially leading to more robust and generalizable models. This could explain why a model trained on real-world data performs better on synthetic data and vice versa.

Performance disparities across different metrics – AP_2D, AP_BEV, AP_3D, and AOS – can be attributed to the complexity of the tasks evaluated by these metrics. AP_3D, which requires full 3D bounding box prediction, is particularly challenging, especially when synthetic training data has limited object instance variance.

These results underscore the need for innovative training methodologies that leverage the benefits of both real-world and synthetic data, such as fine-tuning or data mixing techniques.