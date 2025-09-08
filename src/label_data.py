from ultralytics import YOLO
import cv2
import os
import argparse
import torch

def convert_labels_to_bbox(label_folder, names):
    """
    Converts YOLO format labels to bounding box format in-place.
    <class_name> <x_min> <y_min> <x_max> <y_max>
    """
    for txt_file in os.listdir(label_folder):
        if not txt_file.endswith(".txt"):
            continue

        file_path = os.path.join(label_folder, txt_file)
        
        with open(file_path, "r") as f:
            lines = f.readlines()

        converted_lines = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) != 5:
                continue

            class_id_int = int(parts[0])
            class_name = names.get(class_id_int)

            if class_name is None:
                print(f"Warning: Class ID {class_id_int} not found in names mapping. Skipping line in {file_path}")
                continue

            x_center, y_center, w, h = map(float, parts[1:])
            x_min = x_center - (w / 2)
            y_min = y_center - (h / 2)
            x_max = x_center + (w / 2)
            y_max = y_center + (h / 2)
            converted_lines.append(f"{class_name} {x_min:.6f} {y_min:.6f} {x_max:.6f} {y_max:.6f}\n")

        with open(file_path, "w") as f:
            f.writelines(converted_lines)
        
        print(f"Converted in-place: {txt_file}")

def process_labels(data_dir, split, model, conf_threshold, iou_threshold):
    image_folder = os.path.join(data_dir, split, 'images')
    label_folder = os.path.join(data_dir, split, 'labels')
    os.makedirs(label_folder, exist_ok=True)

    all_image_paths = sorted([os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(('.jpg', '.png', '.jpeg'))])
    
    if not all_image_paths:
        raise ValueError(f"No images found in folder: {image_folder}")

    # Process all images in a batch using model.predict(), use gpu if available, if not use CPU
    results_list = model.predict(all_image_paths, conf=conf_threshold, iou=iou_threshold, device=0 if torch.cuda.is_available() else 'cpu')

    for img_path, results in zip(all_image_paths, results_list):
        image_name = os.path.basename(img_path)
        frame_name, _ = os.path.splitext(image_name)

        # Create YOLO format labels
        labels = []
        for box, cls in zip(results.boxes.xywhn, results.boxes.cls):
            labels.append(f"{int(cls)} {box[0]} {box[1]} {box[2]} {box[3]}")
        
        # Save labels if detections are made
        if labels:
            label_path = os.path.join(label_folder, f'{frame_name}.txt')
            with open(label_path, 'w') as f:
                f.write('\n'.join(labels))
        
        print(f"[INFO] Processed image: {image_name} in {split} set")

    # Convert the generated labels to the bbox format
    print(f"\n--- Converting labels for {split} set ---")
    names = model.model.names
    convert_labels_to_bbox(label_folder, names)
    print(f"--- Finished converting labels for {split} set ---\n")

def generate_labels_and_yaml(data_dir, base_model, conf_threshold, iou_threshold):
    # Initialize YOLO model
    model = YOLO(base_model)
    
    # Process both train and validation folders
    process_labels(data_dir, 'train', model, conf_threshold, iou_threshold)
    process_labels(data_dir, 'valid', model, conf_threshold, iou_threshold)
    
    # Create YAML file
    yaml_content = f"""
path: {os.path.abspath(data_dir)}  # dataset root dir
train: {"train/images"}
val: {"valid/images"}

# Classes
names: {model.model.names}  # using class names from base model
"""
    
    with open(os.path.join(data_dir, 'dataset.yaml'), 'w') as f:
        f.write(yaml_content)
    print("[INFO] YAML file created successfully.")

if __name__ == "__main__":
    data_dir = "labelled_data"

    parser = argparse.ArgumentParser(description="Generate labels for a dataset using a base model and convert them to bounding box format.")

    parser.add_argument("--base_model", default="yolo_models/teacher.pt", help="Path to the pre-trained teacher model (e.g., 'yolo_models/teacher.pt').")
    parser.add_argument("--conf_threshold", type=float, default=0.25, help="Confidence threshold for detections.")
    parser.add_argument("--iou_threshold", type=float, default=0.7, help="IoU threshold for non-max suppression.")
    
    args = parser.parse_args()

    generate_labels_and_yaml(data_dir, args.base_model, args.conf_threshold, args.iou_threshold)