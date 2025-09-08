from ultralytics import YOLO
import cv2
import os
import argparse
import torch

def generate_bbox(image_paths, label_folder, model, conf_threshold, iou_threshold):
    if not image_paths:
        return

    # Process all images in a batch using model.predict(), use gpu if available
    device = 0 if torch.cuda.is_available() else 'cpu'
    results_list = model.predict(image_paths, conf=conf_threshold, iou=iou_threshold, device=device)

    for img_path, results in zip(image_paths, results_list):
        image_name = os.path.basename(img_path)
        frame_name, _ = os.path.splitext(image_name)
        
        # Skip if no detections
        if len(results.boxes) == 0:
            continue

        # Get class names from model
        names = model.model.names
        
        # Create bounding box format labels (xmin, ymin, xmax, ymax)
        labels = []
        for box, cls in zip(results.boxes.xywhn, results.boxes.cls):
            class_id = int(cls)
            class_name = names.get(class_id)
            
            if class_name is None:
                print(f"Warning: Class ID {class_id} not found in names mapping. Skipping.")
                continue
                
            # Convert from YOLO format to bbox format
            x_center, y_center, w, h = box.tolist()
            x_min = max(0, x_center - (w / 2))
            y_min = max(0, y_center - (h / 2))
            x_max = min(1, x_center + (w / 2))
            y_max = min(1, y_center + (h / 2))
            
            labels.append(f"{class_name} {x_min:.6f} {y_min:.6f} {x_max:.6f} {y_max:.6f}")

        # Save the bbox files
        label_path = os.path.join(label_folder, f'{frame_name}.txt')
        with open(label_path, 'w') as f:
            f.write('\n'.join(labels))
        
        print(f"[INFO] Processed image: {image_name}")

def generate_labels(data_dir, split, model, conf_threshold, iou_threshold):
    #Generate labels for all images in a given folder (train or valid)
    image_folder = os.path.join(data_dir, split, 'images')
    label_folder = os.path.join(data_dir, split, 'labels')
    os.makedirs(label_folder, exist_ok=True)

    # Get all images in the folder
    all_image_paths = sorted([os.path.join(image_folder, img) for img in os.listdir(image_folder) 
                            if img.lower().endswith(('.jpg', '.png', '.jpeg'))])
    
    generate_bbox(all_image_paths, label_folder, model, conf_threshold, iou_threshold)


def process_directory(data_dir, base_model, conf_threshold, iou_threshold):
    """Generate labels and YAML configuration for the dataset using the labelled_data folder structure"""
    print(f"[INFO] Loading model: {base_model}")
    # Initialize YOLO model
    model = YOLO(base_model)
    
    # Process both train and validation folders
    generate_labels(data_dir, 'train', model, conf_threshold, iou_threshold)
    generate_labels(data_dir, 'valid', model, conf_threshold, iou_threshold)
    
    # Create YAML file with fixed paths for labelled_data structure
    yaml_content = f"""
path: {os.path.abspath(data_dir)}  # dataset root dir
train: train/images
val: valid/images

# Classes
names: {model.model.names}  # using class names from base model
"""
    
    with open(os.path.join(data_dir, 'dataset.yaml'), 'w') as f:
        f.write(yaml_content)
    print("YAML file created successfully in the labelled_data directory.")

if __name__ == "__main__":
    data_dir = "labelled_data"
    
    parser = argparse.ArgumentParser(description="Generate bounding box labels (xmin, ymin, xmax, ymax format) for images using a YOLO model")

    parser.add_argument("--base_model", default="yolo_models/teacher.pt", 
                      help="Path to the pre-trained YOLO model (e.g., 'yolo_models/teacher.pt').")
    parser.add_argument("--conf_threshold", type=float, default=0.25, 
                      help="Confidence threshold for detections.")
    parser.add_argument("--iou_threshold", type=float, default=0.7, 
                      help="IoU threshold for non-max suppression.")
    
    args = parser.parse_args()
        
    process_directory(data_dir, args.base_model, args.conf_threshold, args.iou_threshold)
    
    print("Label generation complete")