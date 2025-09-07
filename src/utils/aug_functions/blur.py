import cv2
import os

def blur_image(img, kernel_size=(3, 3)): #(3,3) represents how "blurred u want da img to be, ODD INTEGERS ONLY "
    
    # Check if the image was loaded successfully
    if img is None:
        print(f"Failed to load image:")
        return
    
    #Blur dat shit bro
    blurred_img = cv2.GaussianBlur(img, kernel_size, 0)

    return blurred_img