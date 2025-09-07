import os
import argparse

def reset_folder(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        #Loop thru folders
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)  # Delete the files, NOT THE FOLDERS
        print(f"All files in '{folder_path}' have been deleted, but folders are preserved.")
    else:
        print(f"'{folder_path}' does not exist or is not a directory.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reset a folder by deleting all its files.")
    parser.add_argument("folder_path", help="The path to the folder to reset.")
    
    args = parser.parse_args()
    
    reset_folder(args.folder_path)