from preprocessing import preprocess_image

image = preprocess_image("dataset/fox.avif")

if image is not None:
    print("Image preprocessed successfully!")
    print(image.shape)