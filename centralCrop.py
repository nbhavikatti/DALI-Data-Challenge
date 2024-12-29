#This is a general solution for cropping based on a central green square!

import cv2 as cv
import numpy as np
import os

#Choose your image:
imgName = 'unseen_img1'
#imgName = 'img1'
#imgName = 'img2'

#Load the image
img = cv.imread(os.path.join('.', 'images', f'{imgName}.png'))
img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

cv.imshow('img', img)
cv.waitKey(0)

lower_green = np.array([80, 24, 20])  
upper_green = np.array([130, 255, 255])  

# Create a mask for the green color
green_mask = cv.inRange(img_hsv, lower_green, upper_green)

cv.imshow('mask', green_mask)
cv.waitKey(0)

# Morphological operations to clean up the mask
kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))  # Smaller kernel to keep squares distinct
mask_cleaned = cv.morphologyEx(green_mask, cv.MORPH_CLOSE, kernel)  # Close gaps
mask_cleaned = cv.morphologyEx(mask_cleaned, cv.MORPH_OPEN, kernel)  # Remove small noise
mask_cleaned = cv.morphologyEx(mask_cleaned, cv.MORPH_CLOSE, cv.getStructuringElement(cv.MORPH_RECT, (5, 5)))

cv.imshow('cleaned mask', mask_cleaned)
cv.waitKey(0)

green_only = cv.bitwise_and(img, img, mask=mask_cleaned)

cv.imshow('green_only', green_only)
cv.waitKey(0)

# Convert the mask to grayscale for use in adaptive thresholding
green_gray = cv.cvtColor(green_only, cv.COLOR_BGR2GRAY)

# Apply Adaptive Thresholding
adaptive_thresh = cv.adaptiveThreshold(
    green_gray, 
    255, 
    cv.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv.THRESH_BINARY, 
    11,  # Block size: size of the pixel neighborhood
    2    # Constant subtracted from the mean
)

cv.imshow("Adaptive Threshold", adaptive_thresh)
cv.waitKey(0)

contours, hierarchy = cv.findContours(adaptive_thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

contourImg = np.zeros_like(green_only)
cv.drawContours(contourImg, contours, -1, (255,255,255), 3)

cv.imshow('contourImg', contourImg)
cv.waitKey(0)

#Generate filtered_contours based on min_area
min_area = 10000 
filtered_contours = [cnt for cnt in contours if cv.contourArea(cnt) > min_area]

largestSquare = None
max_area = 0

#Loop through each filtered contour
for i, contour in enumerate(filtered_contours):
    area = cv.contourArea(contour)
    x, y, w, h = cv.boundingRect(contour)

    blank_image = np.zeros_like(green_only)
    cv.rectangle(blank_image, (x, y), (x + w, y + h), (255, 255, 255), 2)  # White bounding box

    #Please uncomment the next 3 lines to see the details of processing all contours!
    #print(f"Contour {i}: Area = {area}, Bounding Box = (x={x}, y={y}, w={w}, h={h})")
    #cv.imshow(f"Bounding Box for Contour {i}", blank_image)
    #cv.waitKey(0)  # Wait for a key press to show the next contour

    aspect_ratio = min(w, h) / max(w, h) # measurement of closeness to square. It will be <= 1, closer to 1 is best
    if aspect_ratio > 0.95 and area > max_area:
        largestSquare = contour
        max_area = area

if largestSquare is not None:
    print("We have a central square!")
    x, y, w, h = cv.boundingRect(largestSquare)

    # Crop the original image using the bounding box
    cropped_image = img[y:y+h, x:x+w]

    # Display the original (for reference) and the star of the show: the cropped image!
    cv.imshow('Original Image', img)
    cv.imshow('Cropped Central Square', cropped_image)
    cv.waitKey(0)

    output_path = os.path.join('.', 'images', f'cropped_{imgName}.png')
    cv.imwrite(output_path, cropped_image)

# Wait for a key press and close all windows 
cv.waitKey(0)

