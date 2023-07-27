## LiDAR Simulation Parameters

The AVX simulation engine uses a JavaScript Object Notation (JSON) parameter file to configure the sensors in a simulation. This file defines vital simulation aspects, such as the sensor types, their configurations, and the desired output format.

For LiDAR sensors, the parameter file lets users define the output data format and optimize simulation engine performance.
### Key Configurations

- **Grid Setting (Subsampling):** It controls the subsampling for each laser beam in a rotating LiDAR setting following a polar pattern. The `radialGridPoints` and `angularGridPoints` define the sample points number along the radial direction and around each radial circle, respectively. The `hasCentralPoint` parameter determines whether an extra ray is fired from the laser beam's center. In this study, both `radialGridPoints` and `angularGridPoints` were set to a single sample point, indicating each laser beam is represented by a single sample.

- **Contribution Output Option:** It was activated to generate ground truth information essential for subsequent training processes. This function allows the identification of the objects detected by the LiDAR during the simulation. 

### AVX LiDAR Sensor Simulation Parameters

Here is the JSON parameter configuration for the AVX simulation:

```json
{
    "sensorSimulationParameters": [{
        "identifier": "lidar",
        "recordingFormat": {
            "lidarRecordingFormat": "TEXT"
        },
        "lidarSimulation": {
            "contribution": true,
            "grid": {
                "polarGrid": {
                    "angularGridPoints": 1,
                    "hasCentralPoint": false,
                    "radialGridPoints": 1
                }
            },
            "waveform": false,
            "numberOfBatches":1
        }
    }]
}
```

This configuration defines the setup and properties of the LiDAR sensor simulation. For more details, Please refer to the [full thesis document](../../../aydin_uzun_ms_thesis.pdf).