#VERY IMPORTANT: CHANGE CLASS NAME IN ROBOFLOW TO REMOVE THE - BETWEEN SPACES
#Also, this part might take some time, so feel free to listen to your favourite music while it runs lmao

import glob
import os
import argparse
from roboflow import Roboflow
from .utils.reset import reset_folder

def upload_dataset(api_key, project_id, batch_name):
    # Initialize Roboflow client
    rf = Roboflow(api_key=api_key)

    # Get the upload project from Roboflow workspace
    workspace = rf.workspace()
    project = workspace.project(project_id)

    file_extension_type = ".jpg"
    # Annotation file path and format (e.g., .coco.json)

    datasets_to_upload = [
        {
            "split_type": "train",
            "img_dir_name": "labelled_data/train/images",
            "anot_dir_name": "labelled_data/train/labels",
        },
        {
            "split_type": "valid",
            "img_dir_name": "labelled_data/valid/images",
            "anot_dir_name": "labelled_data/valid/labels",
        }
    ]

    for dataset in datasets_to_upload:
        split_type = dataset["split_type"]
        img_dir_name = dataset["img_dir_name"]
        anot_dir_name = dataset["anot_dir_name"]
        actual_batch_name = f"{batch_name}_{split_type}"

        print(f"--- Uploading {split_type} dataset with batch name {actual_batch_name} ---")

        # image file paths collection
        image_glob = glob.glob(os.path.join(img_dir_name, '*' + file_extension_type))

        for image_path in image_glob:
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            txt_path = os.path.join(anot_dir_name, base_name + ".txt")
            if os.path.isfile(txt_path):
                print(f"Uploading {image_path} with annotation {txt_path}")
                project.single_upload(
                    image_path=image_path,
                    annotation_path=txt_path,
                    batch_name=actual_batch_name,
                    annotation_overwrite=True,
                    split=split_type
                )
            else:
                print(f"Uploading {image_path} without annotation")
                project.single_upload(
                    image_path=image_path,
                    annotation_path=None,
                    batch_name=actual_batch_name,
                    split=split_type
                )
        print(f"--- Finished uploading {split_type} dataset ---")

def main():
    parser = argparse.ArgumentParser(description="Upload a dataset to Roboflow.")
    parser.add_argument("--api_key", required=True, help="Your Roboflow API key.")
    parser.add_argument("--project_id", required=True, help="Your Roboflow project ID (INCLUDE THE CODE AT THE END)")
    parser.add_argument("--batch_name", required=True, help="The batch names for the upload batches.")

    args = parser.parse_args()
    
    upload_dataset(args.api_key, args.project_id, args.batch_name)
    

if __name__ == '__main__':
    main()
    reset_folder("labelled_data")

