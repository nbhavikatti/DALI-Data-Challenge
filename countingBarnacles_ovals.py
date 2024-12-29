#This was my second attempt at counting barnacles - it is a bit more accurate than using circles.

import cv2 as cv
import numpy as np
import os

#Choose your cropped image:
cropped_img_name = 'cropped_unseen_img1'
#cropped_img_name = 'cropped_img1'
#cropped_img_name = 'cropped_img2'
#cropped_img_name = 'unseen_img2'

img = cv.imread(os.path.join('.', 'images', f'{cropped_img_name}.png'))
img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
assert img is not None, "file could not be read, check with os.path.exists()"

img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('image gray', img_gray)
cv.waitKey(0)
img_blurred = cv.GaussianBlur(img_gray, (7, 7), 0)  # Apply Gaussian blur
edges = cv.Canny(img_blurred, 50, 150)  # Edge detection

cv.imshow('edges image', edges)
cv.imshow('original image', img)
cv.waitKey(0)

# Find contours
contours, _ = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

numBarnacles = 0
greaterThan5 = 0

# Create a black image with the same size as the original image
black_background = np.zeros_like(img)

# Create a black image with the same size as the original image
contour_background = np.zeros_like(img)

# List to store bounding boxes of valid ellipses
bounding_boxes = []

# Loop through contours and fit ellipses
for contour in contours:
    # We need at least 5 points to fit an ellipse
    if len(contour) >= 50:

        greaterThan5 += 1
        cv.drawContours(black_background, [contour], -1, (255, 255, 255), 2)  # White color for contours

        ellipse = cv.fitEllipse(contour)
        center, axes, angle = ellipse

        area = np.pi * axes[0] * axes[1]
        max_area = 8000

        if (0.4 < axes[0] / axes[1] < 1.0) and (area < max_area): 
            # Get the bounding box for the ellipse
            (x, y), (major, minor), angle = ellipse
            rect = cv.boundingRect(contour)  # Get the bounding rectangle for the contour

            # Check if the bounding box overlaps with any previously detected bounding boxes
            overlap = False
            for (bx, by, bw, bh) in bounding_boxes:
                # Check for intersection of bounding boxes
                if (rect[0] < bx + bw and rect[0] + rect[2] > bx and
                    rect[1] < by + bh and rect[1] + rect[3] > by):
                    overlap = True
                    break
            
            if not overlap:
                cv.drawContours(contour_background, [contour], -1, (255, 0, 0), 2)
                # Draw the ellipse on the original image and increase the barnacle count
                cv.ellipse(img, ellipse, (255, 0, 0), 2)
                bounding_boxes.append(rect)  # Store the bounding box
                numBarnacles += 1 
            
# Show result
print("Number of Barnacles (ovals) detected: " + str(numBarnacles))
cv.imshow('Contours with >5 Points', black_background)
cv.imshow('Mask with Ovals', contour_background)
cv.imshow('Masked original image with ovals', img)

#Please note: for the final image that pops up (the masked original image), move it to the right to see the mask on the left.
cv.waitKey(0)