import sqlite3
import os
import pickle

from preprocessing import preprocess_image
from feature_extraction import extract_features

DATABASE = "database/images.db"
DATASET_FOLDER = "dataset"

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

extensions = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tif",
    ".tiff",
    ".gif",
    ".webp"
)

count = 0

for file in os.listdir(DATASET_FOLDER):

    if file.lower().endswith(extensions):

        image_path = os.path.join(DATASET_FOLDER, file)

        image = preprocess_image(image_path)

        if image is None:
            continue

        color_feature, shape_feature, texture_feature, feature_vector = extract_features(image)

        color_blob = pickle.dumps(color_feature)
        shape_blob = pickle.dumps(shape_feature)
        texture_blob = pickle.dumps(texture_feature)
        feature_blob = pickle.dumps(feature_vector)

        cursor.execute(
            "SELECT image_name FROM Images WHERE image_name=?",
            (file,)
        )

        if cursor.fetchone():
            print(file, "already exists")
            continue

        cursor.execute("""
        INSERT INTO Images
        (
            image_name,
            image_path,
            color_feature,
            shape_feature,
            texture_feature,
            feature_vector
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            file,
            image_path,
            color_blob,
            shape_blob,
            texture_blob,
            feature_blob
        ))

        count += 1

conn.commit()
conn.close()

print(count, "new images stored successfully!")