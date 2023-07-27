import os
import sys

# Define the path to the folder containing the subdirectories
folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Get the name of the chosen subdirectory from the command line arguments
subdir_name = os.path.basename(os.path.normpath(sys.argv[1]))
chosen_subdir = os.path.join(folder_path, subdir_name, "lidar")

# Define the path to a new directory called "Modified" inside chosen_subdir, and create it if it doesn't already exist
modified_dir = os.path.join(chosen_subdir, "Modified")
if not os.path.exists(modified_dir):
    os.mkdir(modified_dir)
    
# Check if Extents.txt exists in chosen_subdir, if it does, move it to the Modified directory
extents_path = os.path.join(chosen_subdir, 'Extents.txt')
if os.path.exists(extents_path):
    os.rename(extents_path, os.path.join(modified_dir, 'Extents.txt'))
else:
    print("Extents.txt does not exist in the chosen subdirectory.")

# Read the contents of the moved Extents.txt file from the Modified directory
with open(os.path.join(modified_dir, 'Extents.txt'), 'r') as f:
    extents_lines = f.read().splitlines()

# Create a dictionary mapping each car name to a list of entity IDs from the Extents.txt file
car_entity_dict = {}
for line in extents_lines:
    tokens = line.split('\t')
    car_name = tokens[0]
    entity_id = tokens[1]
    if car_name in car_entity_dict:
        car_entity_dict[car_name].append(entity_id)
    else:
        car_entity_dict[car_name] = [entity_id]
    
# Read the contents of the lidar_ContributionDictionary.txt file, convert each line to a dictionary, and add it to a list
with open(os.path.join(chosen_subdir, 'lidar_ContributionDictionary.txt'), 'r') as f:
    file_lines = f.read().splitlines()
entity_list = []
for line in file_lines:
    entity_dict = eval(line)
    entity_list.append(entity_dict)

# Create a dictionary mapping each car instance name to a list of entity IDs from the lidar_ContributionDictionary.txt file
car_instance_dict = {}
for entity_dict in entity_list:
    instance_name = entity_dict['assetDescription']['instanceName']
    entity_id = str(entity_dict['EntityID'])
    if instance_name in car_entity_dict:
        if instance_name in car_instance_dict:
            car_instance_dict[instance_name].append(entity_id)
        else:
            car_instance_dict[instance_name] = [entity_id]

# Write the contents of the car_instance_dict to a new IDs.txt file in the Modified directory
txt_file_path = os.path.join(modified_dir, "IDs.txt")
with open(txt_file_path, 'w') as f:
    for car_name, entity_ids in car_instance_dict.items():
        f.write(f"{car_name}: {entity_ids}\n")

print("Conversion complete!")
