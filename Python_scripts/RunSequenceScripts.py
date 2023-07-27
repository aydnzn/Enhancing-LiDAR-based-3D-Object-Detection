import os  # For operating system dependent functionalities
import subprocess  # To run shell commands
import sys  # To use command line arguments

# Get the directory paths to be processed. 
# Could be provided as command line argument, but in this case, 
# it's hardcoded in the script itself as an example.
# directory_paths = sys.argv[1:]  # Uncomment to get paths from command line
######################################### Directory Paths for Evaluation
# directory_paths = ['MCity Flat AVX v12', 'MCity Flat AVX v13', 'MCity Flat AVX v14', 'MCity Flat AVX v15', 'MCity Flat AVX v16',
#            'MCity Flat AVX v17', 'MCity Flat AVX v18', 'MCity Flat AVX v19', 'MCity Flat AVX v20', 'Highway Japan AVX v2', 'Highway Japan AVX v3',
#            'Highway Japan AVX v4', 'Highway Japan AVX v5', 'Highway Japan AVX v6', 'Highway Japan AVX v7','Highway Japan AVX v8',
#            'Highway Japan AVX v10','Highway Japan AVX v11','Highway Japan AVX v12','Highway Japan AVX v13','Highway Japan AVX v14',
#            'Country AVX v21','Country AVX v22','Country AVX v23','City AVX v8','City AVX v9','City AVX v10','City AVX v11','City AVX v12','City AVX v13','City AVX v14']
###########################################################################################
######################################### Directory Paths for Train
# directory_paths = ['WS03', 'Bridge Concrete AVX','Bridge Steel AVX', 'City AVX','Country AVX', 
#            'Country LHT AVX', 'Country Meander','Country US AVX', 'Highway AVX', 'Highway Japan AVX', 
#            'City AVX v2.2', 'City AVX v3', 'City AVX v4', 'City AVX v5', 'City AVX v6',
#            'MCity Flat AVX v2','City AVX v7','Bridge Steel AVX v2',
#            'Country Meander v2','Country Meander v3','Country Meander v4','Country Meander v5',
#            'Country AVX v2','Country AVX v3','Country AVX v4','Country AVX v5','Country AVX v6', 'Country AVX v7', 'Country AVX v8',
#            'Country AVX v9','Country AVX v10','Country AVX v11','Country AVX v12','Country AVX v13',
#            'Highway AVX v2','Highway AVX v3','Highway AVX v4', 'Highway AVX v5','Highway AVX v6','MCity Flat AVX v3','MCity Flat AVX v4',
#            'MCity Flat AVX v5','MCity Flat AVX v6','MCity Flat AVX v7','MCity Flat AVX v8','MCity Flat AVX v9','MCity Flat AVX v10','MCity Flat AVX v11',
#            'Highway AVX v7','Highway AVX v8','Highway AVX v9','Highway AVX v10',
#            'Bridge Concrete AVX v4','Bridge Concrete AVX v5','Bridge Concrete AVX v6','Bridge Concrete AVX v7','Bridge Concrete AVX v8','Bridge Concrete AVX v9','Bridge Concrete AVX v10',
#            'Country AVX v14','Country AVX v15','Country AVX v16','Country AVX v17','Country AVX v18','Country AVX v19','Country AVX v20']
###########################################################################################
directory_paths = ['scenario_test']  # Define your directories here

# Iterate through each directory path provided
for directory_path in directory_paths:
    # Compute the absolute path of the parent directory of this script file
    folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # Check if the directory exists, exit the script if not
    if not os.path.exists(os.path.join(folder_path, directory_path)):
        print("Directory does not exist: ", directory_path)
        sys.exit(1)

    # List of scripts to be run sequentially
    script_names = ['IdenticalPointCloudDeletion.py', 'PointCloudTxtToNpyConverter.py', 
                    'JsonToTxtConverter.py', 'ExtractInstanceDimensions.py', 
                    'GenerateInstanceEntityIDMapping.py', 'LidarPointCloudLabelGenerator.py', 
                    'PrepareLidarData.py']

    # Loop over the script names and run each one using subprocess.run()
    for script_name in script_names:
        # Run the script using subprocess.run and capture the output
        result = subprocess.run(['python', script_name, directory_path], capture_output=True, text=True)
        
        # Print the output of the script
        print(f"Output of {script_name}:")
        print(result.stdout)  # Standard output (stdout)
        print(result.stderr)  # Standard error (stderr), if any
