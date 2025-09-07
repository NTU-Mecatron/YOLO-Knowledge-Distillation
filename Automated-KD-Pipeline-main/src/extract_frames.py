import os
import argparse
from utils.video_extraction import extract_frames
from utils.reset import reset_folder

original_frame_path = "images/original_frames"
global_f = 0
if __name__ == "__main__":

    reset_folder(original_frame_path)
    parser = argparse.ArgumentParser(description="Extract frames from all videos in 'videos' folder at a specified FPS.")
    parser.add_argument('--target_fps', type=int, default=3, help='Target frames per second for video extraction.')

    args = parser.parse_args()
    target_fps = args.target_fps

    for filename in os.listdir('videos'):
        if filename.endswith((".mp4", ".avi", ".mov", ".mkv")):  # Add more formats if needed
            video_path = os.path.join('videos', filename)
            print(video_path)
            global_f = extract_frames(video_path, original_frame_path, target_fps, global_f) #extract the frames at target_fps    