# Pre-training and Training Duration Impact on 3D AP Scores Analysis

This analysis delves into the effects of pre-training duration on the AP_3D scores for 'Car' and 'Cyclist' categories during training. The scenarios in focus:

1. Training solely on 10% of the KITTI dataset.
2. Pre-training on the AVX dataset, then fine-tuning on 10% of the KITTI dataset.

Pre-training elevates the AP_3D scores from 66.02 (Car) and 49.93 (Cyclist) to 69 and 52.93, respectively. This performance boost suggests the vital role of pre-training in improving model performance.

The readme also explores the scenario where model parameters are saved after every tenth epoch and evaluated on the KITTI dataset. The AP_3D scores achieved within less than 10 minutes for 10 epochs indicate the efficiency of training time, with competitive scores being achieved far quicker compared to 80 epochs, which take approximately 43 minutes.

<figure>
  <img src="../figs/fig1.png" alt="">
  <figcaption>Performance comparison of different training approaches on the AP 3D scores for ’Car’ and ’Cyclist’</figcaption>
</figure>

Above figures show that pre-training followed by fine-tuning yields competitive scores as early as the tenth epoch, emphasizing the significance of synthetic data in quickly optimizing parameters and adapting perception systems for real-time use.
