from ultralytics import YOLO
from utils.reset import recreate_folder
import os
import argparse
import torch

def generate_labels(data_dir: str, model: YOLO, conf: float, iou: float) -> None:
    # Generate bounding box labels for images in a folder
    image_folder = os.path.join(data_dir, 'images')
    label_folder = os.path.join(data_dir, 'labels')
    recreate_folder(label_folder)

    # Get all da image paths
    all_image_paths = [os.path.join(image_folder, img) for img in os.listdir(image_folder) 
                      if img.lower().endswith(('.jpg', '.png', '.jpeg'))]
    
    if not all_image_paths:
        return  # No images to process
    
    print(f"Performing prediction on {len(all_image_paths)} images in {image_folder}...")

    # Set device for prediction
    device = 0 if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")
    names = model.model.names
    print(f"Model class names: {names}")
    
    # Process each image individually
    for i, img_path in enumerate(all_image_paths, 1):
        print(f"Processing image {i}/{len(all_image_paths)}: {os.path.basename(img_path)}")
        
        # Run prediction on single image
        results = model.predict(img_path, conf=conf, iou=iou, device=device, verbose=False)[0]
        
        if len(results.boxes) == 0:
            print(f"No detections found")

        # Get image name WITHOUT extension
        frame_name = os.path.splitext(os.path.basename(img_path))[0]
        
        # Create labels in bbox format
        labels = []
        for box, cls in zip(results.boxes.xywhn, results.boxes.cls):
            labels.append(f"{cls} {box[0]:.6f} {box[1]:.6f} {box[2]:.6f} {box[3]:.6f}")

        # Save labels if there are any 
        # if labels:
        label_path = os.path.join(label_folder, f'{frame_name}.txt')
        with open(label_path, 'w') as f:
            f.write('\n'.join(labels))
        print(f"  Saved {len(labels)} detections to {frame_name}.txt")


def run(data_dir: str, teacher_model: str, conf: float, iou: float):
    """Generate labels and YAML configuration for the dataset"""
    print(f"[INFO] Loading model: {teacher_model}")
    
    # Initialize YOLO model
    model = YOLO(teacher_model)
    generate_labels(data_dir, model, conf, iou)
    
    # Create YAML file
    yaml_content = f"""
dataset: {data_dir}
train: train/images
val: valid/images

# Classes
nc: {len(model.model.names)}
names: {list(model.model.names.values())}
"""
    
    with open(os.path.join(data_dir, 'dataset.yaml'), 'w') as f:
        f.write(yaml_content)
    print("[INFO] YAML file created successfully")

if __name__ == "__main__":

    #don't edit this path
    image_dir = "generated_images/processed"
    
    parser = argparse.ArgumentParser(description="Generate bounding box labels for images using a YOLO model")
    
    parser.add_argument("--teacher_model", default="yolo_models/teacher.pt", help="Path to the pre-trained YOLO model.")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold for detections.")
    parser.add_argument("--iou", type=float, default=0.7, help="IoU threshold for non-max suppression.")
    
    args = parser.parse_args()
    run(image_dir, args.teacher_model, args.conf, args.iou)