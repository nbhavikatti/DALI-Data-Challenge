#This was my first attempt at counting barnacles using HoughCircles.

import cv2 as cv
import numpy as np
import os

#Choose your cropped image:
cropped_img_name = 'cropped_unseen_img1'
#cropped_img_name = 'cropped_img1'
#cropped_img_name = 'cropped_img2'
#cropped_img_name = 'unseen_img2'

img = cv.imread(os.path.join('.', 'images', f'{cropped_img_name}.png'))
assert img is not None, "file could not be read, check with os.path.exists()"
img_gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
img_blurred = cv.GaussianBlur(img_gray, (7, 7), 0)  # Apply Gaussian blur
edges = cv.Canny(img_blurred, 50, 150)  # Edge detection

cv.imshow('edges image', edges)
cv.waitKey(0)

circles = cv.HoughCircles(edges,cv.HOUGH_GRADIENT,1.0,15,param1=100,param2=30,minRadius=0,maxRadius=30)

circles = np.uint16(np.around(circles))

# List to store bounding boxes of circles to check for overlap
bounding_boxes = []

# Create a black image with the same size as the original image
contour_background = np.zeros_like(img)

def check_intersection(bb1, bb2):
    # bb1 and bb2 are tuples (x1, y1, x2, y2) representing the bounding boxes
    # Check if the two bounding boxes intersect
    return not (bb1[2] < bb2[0] or bb1[0] > bb2[2] or bb1[3] < bb2[1] or bb1[1] > bb2[3])

for i in circles[0,:]:
    center = (i[0], i[1])  # Center of the circle
    radius = i[2]  # Radius of the circle
    
    # Calculate the bounding box of the circle (x1, y1, x2, y2)
    x1 = center[0] - radius
    y1 = center[1] - radius
    x2 = center[0] + radius
    y2 = center[1] + radius
    bounding_box = (x1, y1, x2, y2)
    
    # Check if the current bounding box intersects with any previously detected bounding box
    overlap = False
    for bb in bounding_boxes:
        if check_intersection(bounding_box, bb):
            overlap = True
            break
    
    # If there's no overlap, add this circle's bounding box and draw it
    if not overlap:
        bounding_boxes.append(bounding_box)
        cv.circle(img, center, radius, (255, 0, 0), 2)  # Draw the outer circle
        cv.circle(contour_background, center, radius, (255, 0, 0), 2)  # Draw the outer circle
    

print("Number of Barnacles (circles) detected:", circles.shape[1])

#visualize image
cv.imshow('Mask with circles', contour_background)
cv.imshow('Masked original image with circles', img)

#Please note: for the final image that pops up (the masked original image), move it to the right to see the mask on the left.
cv.waitKey(0)
 



