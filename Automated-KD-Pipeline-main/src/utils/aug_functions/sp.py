import os
import numpy as np
from skimage import io, util

def saltAndPepper(img): 
    # Apply salt and pepper noise
    aug_img = util.random_noise(img, mode="s&p", amount = 0.001)
    
    # Convert to uint8 and scale to [0, 255]
    aug_img = (aug_img * 255).astype(np.uint8)
    
    # Return the augmented image for further processing
    return aug_img

