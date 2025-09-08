from ultralytics import YOLO
import cv2
import os
import argparse
import torch

def generate_labels(data_dir, split, model, conf_threshold, iou_threshold):
    # Generate bounding box labels for images in a folder
    image_folder = os.path.join(data_dir, split, 'images')
    label_folder = os.path.join(data_dir, split, 'labels')
    os.makedirs(label_folder, exist_ok=True)

    # Get all da image paths
    all_image_paths = [os.path.join(image_folder, img) for img in os.listdir(image_folder) 
                      if img.lower().endswith(('.jpg', '.png', '.jpeg'))]
    
    if all_image_paths:
        print(f"Processing {split} set images...")
        
        # Run model prediction on all images
        device = 0 if torch.cuda.is_available() else 'cpu'
        results_list = model.predict(all_image_paths, conf=conf_threshold, iou=iou_threshold, device=device)
        names = model.model.names
        
        # Process results and save labels
        for img_path, results in zip(all_image_paths, results_list):
            if len(results.boxes) == 0:
                continue

            # Get image name WITHOUT extension
            frame_name = os.path.splitext(os.path.basename(img_path))[0]
            
            # Create labels in bbox format
            labels = []
            for box, cls in zip(results.boxes.xywhn, results.boxes.cls):
                class_id = int(cls)
                class_name = names.get(class_id)
                
                if class_name is None:
                    continue

                # Convert to xyxy format (x_min, y_min, x_max, y_max)
                x_center, y_center, w, h = box.tolist()
                x_min = max(0, x_center - (w / 2))
                y_min = max(0, y_center - (h / 2))
                x_max = min(1, x_center + (w / 2))
                y_max = min(1, y_center + (h / 2))
                
                labels.append(f"{class_name} {x_min:.6f} {y_min:.6f} {x_max:.6f} {y_max:.6f}")

            # Save labels if there are any 
            if labels:
                label_path = os.path.join(label_folder, f'{frame_name}.txt')
                with open(label_path, 'w') as f:
                    f.write('\n'.join(labels))
        
        print(f"Finished {split} set")


def process_directory(data_dir, base_model, conf_threshold, iou_threshold):
    """Generate labels and YAML configuration for the dataset"""
    print(f"[INFO] Loading model: {base_model}")
    
    # Initialize YOLO model
    model = YOLO(base_model)
    
    # Process both train and validation folders
    generate_labels(data_dir, 'train', model, conf_threshold, iou_threshold)
    generate_labels(data_dir, 'valid', model, conf_threshold, iou_threshold)
    
    # Create YAML file
    yaml_content = f"""
path: {os.path.abspath(data_dir)}
train: train/images
val: valid/images

# Classes
names: {model.model.names}
"""
    
    with open(os.path.join(data_dir, 'dataset.yaml'), 'w') as f:
        f.write(yaml_content)
    print("[INFO] YAML file created successfully")

if __name__ == "__main__":

    #don't edit this path
    data_dir = "labelled_data"
    
    parser = argparse.ArgumentParser(description="Generate bounding box labels for images using a YOLO model")
    
    parser.add_argument("--base_model", default="yolo_models/teacher.pt", 
                      help="Path to the pre-trained YOLO model.")
    parser.add_argument("--conf_threshold", type=float, default=0.25, 
                      help="Confidence threshold for detections.")
    parser.add_argument("--iou_threshold", type=float, default=0.7, 
                      help="IoU threshold for non-max suppression.")
    
    args = parser.parse_args()

    
    process_directory(data_dir, args.base_model, args.conf_threshold, args.iou_threshold)
    
    print("Done")