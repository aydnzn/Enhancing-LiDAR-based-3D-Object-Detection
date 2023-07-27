import os
import json
import sys

# Define the absolute path to the parent folder
folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Extract the name of the subdirectory from the script argument
subdir_name = os.path.basename(os.path.normpath(sys.argv[1]))
# Form the full path to the chosen subdirectory
chosen_subdir = os.path.join(folder_path, subdir_name, "lidar")

# Loop over all .json files in the chosen subdirectory
for filename in os.listdir(chosen_subdir):
    if filename.endswith(".json"):
        json_path = os.path.join(chosen_subdir, filename)
        # Open the .json file and load its contents
        with open(json_path, 'r') as f:
            data = json.load(f)
            # Extract the 'items' from the .json data
            text = data['items']
            
            # Create a corresponding .txt filename
            text_file = filename.replace(".json", ".txt")
            text_path = os.path.join(chosen_subdir, text_file)
            
            # Open the new .txt file and write each 'item' on a new line
            with open(text_path, 'w') as f:
                for item in text:
                    f.write(str(item) + '\n')
            
# Print a success message
print("Conversion complete!")
