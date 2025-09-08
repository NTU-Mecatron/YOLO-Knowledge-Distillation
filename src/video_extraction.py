import cv2
import os
import argparse
from utils.reset import reset_folder

def extract_frames(video_path, output_dir, target_fps, global_frame_count):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return global_frame_count

    video_fps = cap.get(cv2.CAP_PROP_FPS)
    if video_fps <= 0:
        print(f"Error: Could not retrieve FPS for {video_path}")
        cap.release()
        return global_frame_count

    frame_interval = max(1, int(video_fps / target_fps))  # Prevent division by zero
    frame_count = 0

    os.makedirs(output_dir, exist_ok=True)

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count % frame_interval == 0:
                frame_path = os.path.join(output_dir, f'frame_{global_frame_count:06d}.jpg')  # Unique global numbering
                cv2.imwrite(frame_path, frame)
                global_frame_count += 1  # Increment global frame count

            frame_count += 1
    finally:
        cap.release()

    return global_frame_count  # Return updated count

if __name__ == "__main__":
    original_frame_path = "images/original_frames"
    global_f = 0
    reset_folder(original_frame_path)
    parser = argparse.ArgumentParser(description="Extract frames from all videos in 'videos' folder at target FPS.")
    parser.add_argument('--target_fps', type=int, default=3, help='Target frames per second for video extraction.')
    parser.add_argument('--video_path', type=str, required=True, help='Path to the video file.')

    args = parser.parse_args()
    target_fps = args.target_fps
    video_path = args.video_path

    global_f = extract_frames(video_path, original_frame_path, target_fps, global_f)