# Data Sets

Throughout this project, terms such as 'Evaluation', 'Testing', 'Test', 'Validation' will be used interchangeably. Similarly, 'AVX data set' and 'synthetic data set' are used synonymously, as are 'KITTI data set' and 'real data set'.

The comparison of the KITTI and AVX data sets, in terms of frame count and object classes, is presented below. The AVX data set only includes three object classes (car, pedestrian, and cyclist) compared to the variety of classes in the KITTI data set. This comparative analysis provides insight into the structure and diversity of the employed data sets.

| Data Set         | Number of Frames | Car   | Pedestrian | Cyclist | Tram | Truck | Van   | Misc | Person Sitting | DontCare |
| ---------------- | ---------------- | ----- | ---------- | ------- | ---- | ----- | ----- | ---- | -------------- | -------- |
| KITTI Train      | 3712             | 14357 | 2207       | 734     | 224  | 488   | 1297  | 337  | 56             | 5399     |
| KITTI Test       | 3769             | 14385 | 2280       | 893     | 287  | 606   | 1617  | 636  | 166            | 5896     |
| AVX Train        | 5981             | 6880  | 3519       | 3140    | -    | -     | -     | -    | -              | -        |
| AVX Test         | 3617             | 6192  | 1475       | 1058    | -    | -     | -     | -    | -              | -        |

In the KITTI data set, the 'DontCare' label identifies regions not relevant for evaluation, such as parts of the image with irrelevant objects or those too small or ambiguous to classify. Tagging these 'DontCare' regions allows the algorithm to focus on areas of relevance, reducing false positives and improving detection performance.

Visual resemblances among specific classes in the KITTI data set are also considered. For example, 'Van' detections aren't classified as false positives when the target class is 'Car', and 'Person sitting' instances aren't treated as false positives for 'Pedestrian' detections. This consideration correctly handles ambiguous or misleading class appearances.

The synthetic AVX data set does not incorporate these features, as it includes only three distinct classes: 'Car', 'Pedestrian', and 'Cyclist'. While 'DontCare' labels would enhance object detection precision, they are not implemented in this study but offer an avenue for future work.

The 'KITTI Train' and 'AVX Train' data sets are used only for training purposes, and the 'KITTI Test' and 'AVX Test' datasets are used solely for testing, validation, and evaluation processes. When terms like 'trained on KITTI' or 'trained on AVX' are used, they signify the usage of the respective train data sets. Similarly, terms such as 'tested on AVX', 'validated on synthetic data', or 'evaluation on AVX' denote the use of 'AVX Test' for these assessment processes. The same applies to the phrases referencing KITTI.

