import os
import cv2
from ultralytics import YOLO

def save_annotated_images(image_folder, output_dir, base_model, conf_threshold=0.3):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # List all images in the folder
    all_images = sorted([img for img in os.listdir(image_folder) if img.endswith(('.jpg', '.png', '.jpeg'))])
    if not all_images:
        raise ValueError(f"No images found in folder: {image_folder}")
    
    model = YOLO(base_model)

    # Process each image
    for image_name in all_images:
        img_path = os.path.join(image_folder, image_name)
        
        # Load the image using OpenCV
        image = cv2.imread(img_path)
        if image is None:
            print(f"[WARNING] Could not load image: {img_path}")
            continue
        
        # Run inference
        results = model(image)
        
        # Draw annotations on the image
        annotated_image = image.copy()
        for r in results:
            for box, cls, conf in zip(r.boxes.xyxy, r.boxes.cls, r.boxes.conf):
                if conf > conf_threshold:
                    # Extract bounding box coordinates
                    x1, y1, x2, y2 = map(int, box)
                    # Draw the box
                    cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    # Put class name and confidence score
                    class_name = r.names[int(cls)]
                    label = f"{class_name}"
                    cv2.putText(annotated_image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Save annotated image
        output_img_path = os.path.join(output_dir, image_name)
        cv2.imwrite(output_img_path, annotated_image)
        print(f"[INFO] Saved annotated image: {output_img_path}")