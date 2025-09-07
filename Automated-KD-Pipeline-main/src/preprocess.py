import cv2
import os
from utils.reset import reset_folder

def resize(image):
    target_size = 640
    h, w = image.shape[:2]
    
    # Calculate the aspect ratio
    scale = target_size / max(h, w)
    new_w, new_h = int(w * scale), int(h * scale)

    # Resize image
    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

    return resized

def preprocess(input_dir, output_dir):

    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        #ensure it's an image file
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
            cv_image = cv2.imread(input_path)
            #error checking 
            if cv_image is None:
                print(f"Skipping {filename}: Unable to read image.")
                continue
            pro_img = resize(cv_image)
            cv2.imwrite(output_path, pro_img)

if __name__ == "__main__":
    
    input_directory = "images/original_frames"
    output_directory = "images/preprocessed_frames"

    reset_folder(output_directory)

    preprocess(input_directory, output_directory)

    reset_folder(input_directory)