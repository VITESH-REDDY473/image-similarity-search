from preprocessing import preprocess_image
from feature_extraction import extract_features
from database_manager import get_all_images
from closest_pair import euclidean_distance


# Maximum distance allowed for similarity
# 0.50 = about 66.67% similarity
# 1.00 = about 50% similarity
MAX_DISTANCE = 1.00

# Number of images to return
TOP_K = 2


def search_similar_image(image_path):

    # Step 1: Preprocess input image
    image = preprocess_image(image_path)

    if image is None:
        return []

    # Step 2: Extract features from input image
    _, _, _, query_feature = extract_features(image)

    # Step 3: Get all images from database
    database_images = get_all_images()

    if len(database_images) == 0:
        return []

    results = []

    # Step 4: Compare input image with every database image
    for img in database_images:

        distance = euclidean_distance(
            query_feature,
            img["feature_vector"]
        )
        similarity = 100 / (1 + distance)
        results.append({
            "image_name": img["image_name"],
            "image_path": img["image_path"],
            "distance": distance,
            "similarity": similarity
        })

    results.sort(key=lambda x: x["distance"])
    similar_results = [
        result
        for result in results
        if result["distance"] <= MAX_DISTANCE
    ]
    if len(similar_results) >= TOP_K:
        return similar_results[:TOP_K]
    return results[:TOP_K]