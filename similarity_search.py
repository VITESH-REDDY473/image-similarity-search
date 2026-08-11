from preprocessing import preprocess_image
from feature_extraction import extract_features
from database_manager import get_all_images
from closest_pair import euclidean_distance


# Maximum distance allowed for a similar image
MAX_DISTANCE = 0.50


def search_similar_image(image_path):

    # Step 1: Preprocess input image
    image = preprocess_image(image_path)

    if image is None:
        return []

    # Step 2: Extract features
    _, _, _, query_feature = extract_features(image)

    # Step 3: Get database images
    database_images = get_all_images()

    if len(database_images) == 0:
        return []

    results = []

    # Step 4: Compare with database images
    for img in database_images:

        distance = euclidean_distance(
            query_feature,
            img["feature_vector"]
        )

        # Calculate similarity percentage
        similarity = 100 / (1 + distance)

        results.append({
            "image_name": img["image_name"],
            "image_path": img["image_path"],
            "distance": distance,
            "similarity": similarity
        })

    # Step 5: Sort by smallest distance
    results.sort(key=lambda x: x["distance"])

    # Step 6: Check best match
    best_result = results[0]

    if best_result["distance"] > MAX_DISTANCE:
        return []

    # Step 7: Return best results
    return results[:5]