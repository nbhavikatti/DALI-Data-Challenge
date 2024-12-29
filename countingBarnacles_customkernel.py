#This is a general (near) solution for detecting and counting barnacles!

import cv2 as cv
import numpy as np
import os

#Choose your cropped image:
cropped_img_name = 'cropped_unseen_img1'
#cropped_img_name = 'cropped_img1'
#cropped_img_name = 'cropped_img2'
#cropped_img_name = 'unseen_img2'

img = cv.imread(os.path.join('.', 'images', f'{cropped_img_name}.png'))
img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
assert img is not None, "file could not be read, check with os.path.exists()"

cv.imshow('ORIGINAL img', img)
cv.waitKey(0)

img_blurred = cv.GaussianBlur(img_gray, (7, 7), 0)  # Apply Gaussian blur
edges = cv.Canny(img_blurred, 30, 150)  # Edge detection

cv.imshow('edges', edges)
cv.waitKey(0)

# Apply a morphological operation
# Morphological kernel
morph_kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))

# Apply MORPH_OPEN to remove noise
morphed_open = cv.morphologyEx(edges, cv.MORPH_CLOSE, morph_kernel)

# Apply MORPH_CLOSE to fill gaps after removing noise
morphed = cv.morphologyEx(morphed_open, cv.MORPH_CLOSE, morph_kernel)

cv.imshow('morphed', morphed)

contours, _ = cv.findContours(morphed, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

# Create a black image to draw the contours on
black_background = np.zeros_like(img)

# Count the number of barnacles based on contours
barnacle_count = 0
for contour in contours:
    # Filter out small contours that are unlikely to be barnacles
    if cv.contourArea(contour) > 115:
        # Fit an ellipse to the contour
        if len(contour) >= 5:  # Fit an ellipse requires at least 5 points
            ellipse = cv.fitEllipse(contour)
            center, axes, angle = ellipse

            # Calculate the aspect ratio (major axis / minor axis of the ellipse)
            aspect_ratio = axes[0] / axes[1]
            perimeter = cv.arcLength(contour, True)
            circularity = (4 * np.pi * cv.contourArea(contour)) / (perimeter ** 2)

            # Filter based on aspect ratio and area of the ellipse
            if 0.4 < aspect_ratio < 1.0 and (circularity > 0.2):
                barnacle_count += 1
                cv.drawContours(img, [contour], -1, (255, 0, 0), 2)  # Draw contours on the original image in blue
                cv.drawContours(black_background, [contour], -1, (255, 0, 0), 2)  # Draw contours on a black background in blue

print("Number of barnacles detected:", barnacle_count)

# Show the result with contours drawn
cv.imshow('Mask', black_background)

output_path = os.path.join('.', 'images', f'masked_{cropped_img_name}.png')
cv.imwrite(output_path, img)

cv.imshow('Masked original image', img)

output_path = os.path.join('.', 'images', f'mask_{cropped_img_name}.png')
cv.imwrite(output_path, black_background)

cv.waitKey(0)