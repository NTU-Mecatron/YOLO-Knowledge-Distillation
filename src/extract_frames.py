import cv2
import os
import argparse
from utils.reset import recreate_folder

def extract_frames(video_path: str, output_dir: str, target_fps: int) -> None:
    """ Extract frames from a video at a specified target FPS. """
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return

    video_fps = cap.get(cv2.CAP_PROP_FPS)
    if video_fps <= 0:
        print(f"Error: Could not retrieve FPS for {video_path}")
        cap.release()
        return

    frame_interval = max(1, int(video_fps / target_fps))  # Prevent division by zero
    frame_count = 0
    saved_count = 0

    os.makedirs(output_dir, exist_ok=True)

    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            break
        
        frame_count += 1
        if frame_count % frame_interval != 0:            
            continue

        frame_path = os.path.join(output_dir, f'frame_{saved_count}.jpg')
        cv2.imwrite(frame_path, frame)
        saved_count += 1

    cap.release()

    print(f"Extracted {saved_count} frames from {video_path}")


def resize_while_maintain_aspect_ratio(image: cv2.Mat) -> cv2.Mat:
    target_size = 640
    h, w = image.shape[:2]
    
    # Calculate the aspect ratio
    scale = target_size / max(h, w)
    new_w, new_h = int(w * scale), int(h * scale)

    # Resize image
    return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

def is_blurry(image: cv2.Mat, threshold: float = 100.0) -> bool:
    """ Determine if an image is blurry using the variance of the Laplacian. The higher the variance, the sharper the image. \n
    Hence, choose higher threshold for stricter condition."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian_var < threshold

def apply_preprocessing(input_dir: str, output_dir: str, blurry_threshold: float) -> None:
    """ Resize within and remove blurry images. """
    filenames = sorted(os.listdir(input_dir))  
    count = 0
    for filename in filenames:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        #ensure it's an image file
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
            continue

        img = cv2.imread(input_path)
        #error checking 
        if img is None:
            print(f"Skipping {filename}: Unable to read image.")
            continue

        if is_blurry(img, blurry_threshold):
            print(f"Skipping {filename}: Image is too blurry.")
            continue
        
        pro_img = resize_while_maintain_aspect_ratio(img)
        cv2.imwrite(output_path, pro_img)
        count += 1
    print(f"Preprocessing complete. {count} images saved to {output_dir}.")

if __name__ == "__main__":
    original_frame_path = "generated_images/original"
    preprocessed_frame_path = "generated_images/processed/images"

    recreate_folder(original_frame_path)
    recreate_folder(preprocessed_frame_path)

    parser = argparse.ArgumentParser(description="Extract frames from all videos in 'videos' folder at target FPS.")
    parser.add_argument('--source', type=str, required=True, help='Path to the video file.')
    parser.add_argument('--fps', type=int, default=2, help='Target frames per second for video extraction.')
    parser.add_argument('--blurry_threshold', type=float, default=100.0, help='Higher for stricter blur detection.')

    args = parser.parse_args()
    target_fps = args.fps
    video_path = args.source
    blurry_threshold = args.blurry_threshold

    extract_frames(video_path, original_frame_path, target_fps)
    apply_preprocessing(original_frame_path, preprocessed_frame_path, blurry_threshold)
