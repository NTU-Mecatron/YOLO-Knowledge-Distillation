import os
import argparse

def reset_folder(folder_path):
    """ Delete all files in the specified folder but keep the folder structure intact. """
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        #Loop thru folders
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)  # Delete the files, NOT THE FOLDERS
        print(f"All files in '{folder_path}' have been deleted, but folders are preserved.")
    else:
        print(f"'{folder_path}' does not exist or is not a directory.")

def recreate_folder(folder_path):
    """ Delete and recreate the directory according to the given path. """
    if os.path.exists(folder_path):
        # Delete the folder and its contents
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(folder_path)
    
    # Recreate the empty folder
    os.makedirs(folder_path)
    print(f"'{folder_path}' has been recreated as an empty folder.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reset a folder by deleting all its files.")
    parser.add_argument("folder_path", help="The path to the folder to reset.")
    
    args = parser.parse_args()
    
    reset_folder(args.folder_path)