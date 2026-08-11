import cv2
import numpy as np


def extract_lbp(gray):

    height, width = gray.shape

    lbp = np.zeros((height, width), dtype=np.uint8)

    for i in range(1, height - 1):
        for j in range(1, width - 1):

            center = gray[i, j]

            code = 0

            code |= (gray[i-1, j-1] >= center) << 7
            code |= (gray[i-1, j] >= center) << 6
            code |= (gray[i-1, j+1] >= center) << 5
            code |= (gray[i, j+1] >= center) << 4
            code |= (gray[i+1, j+1] >= center) << 3
            code |= (gray[i+1, j] >= center) << 2
            code |= (gray[i+1, j-1] >= center) << 1
            code |= (gray[i, j-1] >= center)

            lbp[i, j] = code

    return lbp


def extract_features(image):

    image = (image * 255).astype(np.uint8)

    # -----------------------
    # Color Feature
    # -----------------------

    color_feature = cv2.calcHist(
        [image],
        [0, 1, 2],
        None,
        [8, 8, 8],
        [0, 256, 0, 256, 0, 256]
    )

    color_feature = cv2.normalize(
        color_feature,
        color_feature
    ).flatten()

    # -----------------------
    # Shape Feature
    # -----------------------

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_RGB2GRAY
    )

    moments = cv2.moments(gray)

    shape_feature = cv2.HuMoments(
        moments
    ).flatten()

    # -----------------------
    # Texture Feature (LBP)
    # -----------------------

    lbp = extract_lbp(gray)

    texture_feature = cv2.calcHist(
        [lbp],
        [0],
        None,
        [256],
        [0, 256]
    )

    texture_feature = cv2.normalize(
        texture_feature,
        texture_feature
    ).flatten()

    # -----------------------
    # Combined Feature Vector
    # -----------------------

    feature_vector = np.concatenate(
        (
            color_feature,
            shape_feature,
            texture_feature
        )
    )

    return (
        color_feature,
        shape_feature,
        texture_feature,
        feature_vector
    )