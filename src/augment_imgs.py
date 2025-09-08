#Augmentation techniques to be implemented: random rotation, salt and pepper noise, and blurs
#basically, take a folder of images and apply aug, and then put them in a different folder 
#also before that, separate train and valid iamges

import os
import cv2
from sklearn.model_selection import train_test_split
import shutil
import random
import os
import argparse
from utils.reset import reset_folder

from utils.aug_functions.blur import blur_image 
from utils.aug_functions.sp import saltAndPepper
from utils.aug_functions.hsv import random_HSV
from utils.aug_functions.flip import flip_horizontal

aug_functions = [blur_image, saltAndPepper, random_HSV, flip_horizontal]


def augment_images(input_folder, train_folder, valid_folder, multiplier, valid_size=0.25): #multiplier refers to how many times you want the size of the aug data to be compared with original size

    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(valid_folder, exist_ok=True)

    all_images = [img for img in os.listdir(input_folder) if img.endswith(('.jpg', '.png', '.jpeg'))]
    if not all_images:
        raise ValueError(f"No images found in folder: {input_folder}")
    
    train_images, valid_images = train_test_split(all_images, test_size=valid_size)
    
    for image_name in valid_images:
        src_img_path = os.path.join(input_folder, image_name)
        dst_img_path = os.path.join(valid_folder, image_name)
        
        shutil.copy(src_img_path, dst_img_path) #move specified percentage (the 0.4 there can be changed) to serve as VALID IMGS
    

    # Process each image
    for image_name in train_images:
        base_name, ext = os.path.splitext(image_name) #split the image into base name and the type of extention (will need it later trust me)
        img_path = os.path.join(input_folder, image_name)
        image = cv2.imread(img_path)

        if image is None:
            print(f"[WARNING] Could not load image: {img_path}")
            continue

        #First of all, save original images, we're still gonna need 'em
        cv2.imwrite(os.path.join(train_folder, image_name), image)

        clean_img = image
        

        for i in range(multiplier): #repeat as many times as specified in the multiplier input
            aug_image = clean_img
            random.shuffle(aug_functions) #shuffle the list of functions 
            for aug_function in aug_functions:
                applyOrNot = random.randint(0,2) #66% chance of applying each aug_function
                if(applyOrNot == 0 or applyOrNot == 1):
                    aug_image = aug_function(aug_image)
            
            aug_image_path = f"{base_name}_aug_{i}_{ext}" #put it as different name by adding aug in the middle
            cv2.imwrite(os.path.join(train_folder, aug_image_path), aug_image)
            print("[INFO] Augmentation completed!")

if __name__ == "__main__":

    origin_folder = "images/original_frames"
    input_folder = "images/preprocessed_frames"
    train_folder = "labelled_data/train/images"
    valid_folder = "labelled_data/valid/images"

    reset_folder(train_folder)
    reset_folder(valid_folder)
    
    parser = argparse.ArgumentParser(description="Augment images in a folder and split into train/valid sets.")
    parser.add_argument('--aug_multiplier', type=int, default=3, help='Augmentation multiplier.')
    parser.add_argument('--valid_size', type=float, default=0.25, help='Validation set size (e.g., 0.2 for 20%).')

    args = parser.parse_args()
    aug_multiplier = args.aug_multiplier
    valid_size = args.valid_size

    augment_images(input_folder, train_folder, valid_folder, aug_multiplier, valid_size)

    reset_folder(origin_folder)
    reset_folder(input_folder)