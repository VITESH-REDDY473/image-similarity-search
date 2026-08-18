import sqlite3
import os

# Create database folder
os.makedirs("database", exist_ok=True)

# Create database
conn = sqlite3.connect("database/images.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_name TEXT,
    image_path TEXT,
    color_feature BLOB,
    shape_feature BLOB,
    texture_feature BLOB,
    feature_vector BLOB
)
""")

conn.commit()
conn.close()

print("Database created successfully!")