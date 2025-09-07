import cv2
import numpy as np
import random

def random_HSV(img):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)  # Use float32 for precise scaling
    
    # Apply ±5% augmentation
    h_scale = 1 + random.uniform(-0.05, 0.05)  # Scale Hue by -5% to +5%
    s_scale = 1 + random.uniform(-0.05, 0.05)  # Scale Saturation by -5% to +5%
    v_scale = 1 + random.uniform(-0.05, 0.05)  # Scale Value (Brightness) by -5% to +5%

    # Apply transformations
    hsv[:, :, 0] = np.clip(hsv[:, :, 0] * h_scale, 0, 179)  # Hue range: [0, 179]
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * s_scale, 0, 255)  # Saturation range: [0, 255]
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] * v_scale, 0, 255)  # Value range: [0, 255]

    # Convert back to uint8
    hsv = hsv.astype(np.uint8)

    # Convert back to BGR
    img_bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    return img_bgr