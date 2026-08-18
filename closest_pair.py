import math

def euclidean_distance(feature1, feature2):
    """
    Calculate Euclidean distance between two feature vectors.
    """
    distance = 0

    for a, b in zip(feature1, feature2):
        distance += (a - b) ** 2

    return math.sqrt(distance)


def find_closest_image(query_feature, database_images):

    best_image = None
    minimum_distance = float("inf")

    for image in database_images:

        distance = euclidean_distance(
            query_feature,
            image["feature_vector"]
        )

        if distance < minimum_distance:
            minimum_distance = distance
            best_image = image

    return best_image, minimum_distance