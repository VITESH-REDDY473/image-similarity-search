import cv2
import numpy as np
from PIL import Image

def preprocess_image(image_path):

    try:
        img = Image.open(image_path).convert("RGB")
        image = np.array(img)

    except Exception as e:
        print("Error reading image:", e)
        return None

    image = cv2.resize(image, (256,256))
    image = cv2.GaussianBlur(image,(5,5),0)
    image = image.astype("float32")/255.0

    return image