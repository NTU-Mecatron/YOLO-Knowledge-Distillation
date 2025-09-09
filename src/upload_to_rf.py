import argparse
from roboflow import Roboflow

def upload_dataset(api_key, project_id, batch_name):
    # Initialize Roboflow client
    rf = Roboflow(api_key=api_key)

    # Get the upload project from Roboflow workspace
    workspace = rf.workspace()
    path_to_dataset = "generated_images/processed"
    datasets_to_upload = [
        {
            "path": path_to_dataset,
            "split_type": "train",
            "img_dir_name": path_to_dataset + "/images",
            "anot_dir_name": path_to_dataset + "/labels",
        }
    ]

    for dataset in datasets_to_upload:
        dataset_path = dataset["path"]
        workspace.upload_dataset(
            dataset_path=dataset_path,
            project_name=project_id,
            num_workers=25,
            dataset_format="yolov8",
            project_license="public",
            batch_name=batch_name,
        )
    print(f"--- Finished uploading dataset(s) ---")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Upload a dataset to Roboflow.")
    parser.add_argument("--api_key", required=True, help="Your Roboflow API key.")
    parser.add_argument("--project_id", required=True, help="Your Roboflow project ID (INCLUDE THE CODE AT THE END)")
    parser.add_argument("--batch_name", required=True, help="The batch names for the upload batches.")

    args = parser.parse_args()
    
    upload_dataset(args.api_key, args.project_id, args.batch_name)