import os  
import shutil 
import argparse 

def copy_selected_checkpoints(source_dir, destination_dir):
    # Create the destination directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)  # Create the destination directory using 'os.makedirs'

    # List the checkpoint files in the source directory
    checkpoint_files = os.listdir(source_dir)  # Get a list of all files in the source directory using 'os.listdir'

    # Select the specific checkpoints you want to copy
    checkpoints_to_copy = [1, 10, 20, 30, 40, 50, 60, 70, 80]

    # Copy the selected checkpoints to the destination directory
    for checkpoint in checkpoints_to_copy:
        checkpoint_file = f"checkpoint_epoch_{checkpoint}.pth"  # Construct the checkpoint file name
        if checkpoint_file in checkpoint_files:
            source_path = os.path.join(source_dir, checkpoint_file)  # Construct the source path using 'os.path.join'
            destination_path = os.path.join(destination_dir, checkpoint_file)  # Construct the destination path using 'os.path.join'
            shutil.copy2(source_path, destination_path)  # Copy the checkpoint file from the source path to the destination path using 'shutil.copy2'

if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Copy selected checkpoints from source to destination directory")

    # Define the command-line argument 'source_dir'
    parser.add_argument("source_dir", type=str, help="Path to the source directory")

    # Parse the command-line argument
    args = parser.parse_args()

    # Define the destination directory path
    parent_dir = os.path.dirname(args.source_dir)  # Get the parent directory of the source directory using 'os.path.dirname'
    destination_dir = os.path.join(parent_dir, 'ckpt_selected')  # Construct the destination directory path using 'os.path.join'

    # Call the function to copy the selected checkpoints
    copy_selected_checkpoints(args.source_dir, destination_dir)  # Call the 'copy_selected_checkpoints' function with the source and destination directory paths
