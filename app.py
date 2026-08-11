from flask import Flask, render_template, request, send_from_directory
import os

from similarity_search import search_similar_image


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
DATASET_FOLDER = "dataset"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
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

    # Save uploaded image
    upload_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(upload_path)

    # Run your existing similarity search
    results = search_similar_image(upload_path)

    # Check result
    if not results:
        return render_template(
            "index.html",
            error="No similar image found."
        )

    # Get best matching image
    best_result = results[0]

    best_image_name = best_result["image_name"]
    distance = best_result["distance"]
    similarity = best_result["similarity"]

    # Display result
    return render_template(
        "index.html",
        input_image=file.filename,
        best_image=best_image_name,
        distance=round(distance, 4),
        similarity=round(similarity, 2)
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