# Adapting KITTI Difficulty Levels for Synthetic Data Set Evaluation

The KITTI data set segments object detection challenges into three separate levels of difficulty: 'Easy,' 'Moderate,' and 'Hard'. The assignment of these levels is based on a set of conditions, which include minimum bounding box height, maximum occlusion, and truncation level.

- **Easy**: This level refers to simpler scenarios. The lower limit for bounding box height is 40 pixels, occlusion is denoted as 'Fully Visible' or 'Partly Occluded,' and truncation is limited to a maximum of 15%.

- **Moderate**: This level incorporates more complexity with smaller objects and higher occlusion levels. The minimum bounding box height in this case is 25 pixels. The occlusion can be 'Fully Visible,' 'Partly Occluded,' or 'Largely Occluded,' and the truncation can be up to 30%.

- **Hard**: This level presents the most challenging scenarios, potentially including small, heavily occluded or truncated objects. The bounding box height limit remains at 25 pixels, any occlusion level is allowed, and truncation can be as high as 50%.

## Modifications for Synthetic Data Set Evaluation

However, when evaluating a synthetic data set, certain adjustments to this approach are necessary. The 'occluded' field in the KITTI label was not considered in the synthetic data set, resulting in all objects being marked as 'fully visible'. This modification means that object occlusions are not taken into account in the synthetic data set evaluation. Therefore, the revised difficulty levels for the synthetic data set only consider the bounding box height and truncation of the objects.

Also, the 'DontCare' label plays a significant role in the evaluation of real data sets. However, this feature is not included during synthetic data set evaluation.
