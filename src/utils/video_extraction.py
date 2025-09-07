import cv2
import os

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