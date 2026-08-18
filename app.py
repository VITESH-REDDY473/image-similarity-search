from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import os

from similarity_search import search_similar_image


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
DATASET_FOLDER = "dataset"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Search similar image
@app.route("/search", methods=["GET", "POST"])
def search():

    # If someone directly opens /search
    if request.method == "GET":
        return render_template("index.html")

    # Check if image was selected
    if "image" not in request.files:
        return render_template(
            "index.html",
            error="Please select an image."
        )

    file = request.files["image"]

    # Check empty filename
    if file.filename == "":
        return render_template(
            "index.html",
            error="Please select an image."
        )

    # Make filename safe
    filename = secure_filename(file.filename)

    # Save uploaded image
    upload_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(upload_path)

    # Search for similar images
    results = search_similar_image(upload_path)

    # Check result
    if not results:
        return render_template(
            "index.html",
            error="No images found in the database."
        )

    # Prepare results for display
    similar_images = []

    for result in results:

        similar_images.append({
            "image_name": result["image_name"],
            "distance": round(result["distance"], 4),
            "similarity": round(result["similarity"], 2)
        })

    # Display results
    return render_template(
        "index.html",
        input_image=filename,
        results=similar_images
    )


# Display uploaded image
@app.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )


# Display dataset image
@app.route("/dataset/<filename>")
def dataset_file(filename):

    return send_from_directory(
        DATASET_FOLDER,
        filename
    )


# Start Flask server
if __name__ == "__main__":
    app.run(debug=True)