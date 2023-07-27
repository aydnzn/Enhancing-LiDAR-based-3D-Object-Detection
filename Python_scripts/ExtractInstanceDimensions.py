import os
import sys

# Define the path to the folder containing the subdirectories
folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
subdir_name = os.path.basename(os.path.normpath(sys.argv[1]))
chosen_subdir = os.path.join(folder_path, subdir_name, "lidar")

# Define instance mapping dictionary
instance_mapping = {'CAR1': 'Car', 'CAR2' : 'Car','CAR3': 'Car', 'CAR4' : 'Car','CAR5': 'Car','CAR6': 'Car','CAR7': 'Car','CAR8': 'Car', 'PED1': 'Pedestrian','PED2': 'Pedestrian', 'PED3': 'Pedestrian', 'PED4': 'Pedestrian', 'BIC1': 'Bicycle', 'BIC2': 'Bicycle', 'BIC3': 'Bicycle', 'BIC4': 'Bicycle'}

# Define model dimensions dictionary
dimensions = {
    'audi_a1_2010_blue':[3.954,1.774,1.474],
    'audi_a1_2010_long_range_blue':[3.954,1.774,1.474],
    'audi_a1_2010_orange':[3.954,1.774,1.474],
    'audi_a1_2010_red':[3.954,1.774,1.474],
    'audi_a1_2010_white':[3.954,1.774,1.474],
    'audi_a3_2013_red' : [4.333,2,1.434],
    'audi_a3_2013_red_engine_running_thermal':[4.333,2,1.434],
    'audi_a3_2013_red_engine_off_thermal':[4.333,2,1.434],
    'audi_a3_sportback_red':[4.3,2.0,1.427],
    'bmw_x5_2009_black':[4.838,2.073,1.896],
    'bmw_x5_2009_blue' :[4.838,2.073,1.896],
    'bmw_x5_2009_grey':[4.838,2.073,1.896],
    'bmw_x5_2009_red':[4.838,2.073,1.896],
    'bmw_x5_2009_white':[4.838,2.073,1.896],
    'citroen_nemo_2007_black':[3.872,1.642,1.715],
    'citroen_nemo_2007_blue':[3.872,1.642,1.715],
    'citroen_nemo_2007_grey':[3.872,1.642,1.715],
    'citroen_nemo_2007_red':[3.872,1.642,1.715],
    'citroen_nemo_2007_white':[3.872,1.642,1.715],
    'dodge_charger_2008_grey':[4.864,1.887,1.515],
    'dodge_charger_2008_red':[4.864,1.887,1.515],
    'dodge_charger_2008_white':[4.864,1.887,1.515],
    'dodge_charger_2008_yellow':[4.864,1.887,1.515],
    'dodge_charger_2018_yellow_engine_running_thermal':[4.864,1.887,1.515],
    'dodge_charger_2018_yellow_engine_off_thermal':[4.864,1.887,1.515],
    'genesis_g80_2017_black': [4.99,2.139, 1.48],
    'genesis_g80_2017_blue': [4.99,2.139, 1.48],
    'jaguar_e_pace_2018_white':[4.542,2.05,1.71],
    'kia_soul_2010_black':[4.077,1.783,1.662],
    'kia_soul_2010_orange':[4.077,1.783,1.662],
    'kia_soul_2010_red':[4.077,1.783,1.662],
    'kia_soul_2010_white':[4.077,1.783,1.662],
    'kia_soul_2010_yellow':[4.077,1.783,1.662],
    'nissan_juke_2013_black':[4.147,1.94,1.568],
    'skoda_octavia_2020_blue':[4.845,2.03,1.486],
    'suzuki_swift_2005_white':[3.653,1.679,1.506],
    'toyota_chr_2017_grey':[4.356,2.033,1.603],
    'toyota_corolla_2017_brown':[4.646,2.1,1.457],
    'toyota_prius_2012_blue': [4.386, 1.758, 1.496 ],
    'toyota_prius_2012_green':[4.386, 1.758, 1.496],
    'toyota_prius_2012_orange':[4.386, 1.758, 1.496],
    'toyota_prius_2012_red':[4.386, 1.758, 1.496],
    'toyota_prius_2012_white':[4.386, 1.758, 1.496],
    'volkswagen_tiguan_2019_blue':[4.475,2.115,1.586],
    'volvo_xc60_2018_blue':[4.85,1.95,1.805],
    'volvo_xc60_2018_blue_simplified_engine_running_thermal':[4.85,1.95,1.805],
    'pedestrian_male': [0.373,0.6,1.781],
    'pedestrian_female': [0.41,0.6,1.664],
    'pedestrian_male_thermal':[0.373,0.6,1.781],
    'pedestrian_female_thermal':[0.41,0.6,1.664],
    'bike': [1.6,0.6,1.58],
            # Add more asset paths and dimensions as needed
}

# Define the path to a new directory called "Modified" inside chosen_subdir, and create it if it doesn't already exist
modified_dir = os.path.join(chosen_subdir, "Modified")
if not os.path.exists(modified_dir):
    os.mkdir(modified_dir)

# Check if the 'Extents.txt' already exists in the chosen or modified directory, if it does print a message and abort, otherwise process the lidar_ContributionDictionary.txt file
if os.path.exists(os.path.join(chosen_subdir, 'Extents.txt')):
    print(f"The file {os.path.join(chosen_subdir, 'Extents.txt')} already exists. Aborting...")
elif os.path.exists(os.path.join(modified_dir, 'Extents.txt')):
    print(f"The file {os.path.join(modified_dir, 'Extents.txt')} already exists. Aborting...")
else:
    instances_written = set()
    with open(os.path.join(chosen_subdir, 'lidar_ContributionDictionary.txt'), 'r') as f, open(os.path.join(chosen_subdir, 'Extents.txt'), 'w') as out:
        # Process each line of the 'lidar_ContributionDictionary.txt' file
        for line in f:
            data = eval(line)  # Convert string to dictionary
            instance_name = data['assetDescription']['instanceName']
            # Check if instance_name is in the mapping and has not been written to output file yet
            if instance_name in instance_mapping and instance_name not in instances_written:
                asset_path = data['assetDescription']['assetPath']
                filename = os.path.basename(asset_path)
                # Find matching keys in the dimensions dictionary
                matching_keys = [key for key in dimensions if filename.startswith(key)]
                # If there are matching keys, write the instance_name and dimensions to the 'Extents.txt' file
                if matching_keys:
                    key = matching_keys[0]  # Assuming there's only one matching key
                    dimensions_str = '\t'.join([f'{d:.3f}' for d in dimensions[key]])
                    out.write(f'{instance_name}\t{dimensions_str}\n')
                    instances_written.add(instance_name)

    print("Extents.txt complete!")
