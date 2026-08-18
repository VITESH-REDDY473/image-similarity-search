from preprocessing import preprocess_image
from feature_extraction import extract_features

# Change this to one of your image names
image = preprocess_image("dataset/dog.jpg")

if image is not None:

    features = extract_features(image)

    print("Feature Extraction Successful")
    print("Feature Vector Length:", len(features))