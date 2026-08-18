import sqlite3
import pickle

DATABASE = "database/images.db"


def get_all_images():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            image_name,
            image_path,
            color_feature,
            shape_feature,
            texture_feature,
            feature_vector
        FROM Images
    """)

    rows = cursor.fetchall()

    conn.close()

    images = []

    for row in rows:

        images.append({

            "image_name": row[0],

            "image_path": row[1],

            "color_feature": pickle.loads(row[2]),

            "shape_feature": pickle.loads(row[3]),

            "texture_feature": pickle.loads(row[4]),

            "feature_vector": pickle.loads(row[5])

        })

    return images