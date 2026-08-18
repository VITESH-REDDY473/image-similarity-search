import os
import sqlite3
from tkinter import Tk, filedialog

# Connect to database
conn = sqlite3.connect("database/images.db")
cursor = conn.cursor()

# Hide the Tkinter window
root = Tk()
root.withdraw()

# Select the dataset folder
folder = filedialog.askdirectory(title="Select Dataset Folder")

if folder:

    # Supported image formats
    extensions = (".jpg", ".jpeg", ".png", ".bmp")

    # Get all image files
    images = [f for f in os.listdir(folder) if f.lower().endswith(extensions)]

    # Limit to 500 images
    if len(images) > 500:
        print("Only the first 500 images will be uploaded.")
        images = images[:500]

    for image in images:

        image_path = os.path.join(folder, image)

        cursor.execute("""
        INSERT INTO Images
        (image_name, image_path)
        VALUES (?, ?)
        """, (image, image_path))

    conn.commit()

    print(f"{len(images)} images uploaded successfully!")

else:
    print("No folder selected.")

conn.close()