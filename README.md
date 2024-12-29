This project leverages centralCrop.py to crop an image based on a central green/blue square and then countingBarnacles_circles.py to count the number of barnacles in a cropped photo (which will be outputted in the terminal). 

## Requirements
- Python 3.x
- OpenCV (`opencv-python`)
- Numpy

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/nbhavikatti/DALI-Data-Challenge.git
    cd DALI-Data-Challenge
    ```

2. Install required dependencies:

    ```bash
    pip install opencv-python numpy
    ```

## Usage

1. Place your images in the `images/` folder.
2. Run the `centralCrop.py` script to crop the image:

    ```bash
    python centralCrop.py
    ```

3. After cropping, run any of the barnacle counting scripts:

    ```bash
    python countingBarnacles_circles.py
    python countingBarnacles_ovals.py
    python countingBarnacles_customkernel.py
    ```

These scripts will process the cropped images and provide the results.

## Files in this project

centralCrop.py takes in an original image, crops it, and writes it to the images folder. 
countingBarnacles_customkernel.py (my third and final attempt) takes a cropped image of barnacles and outputs to the terminal an estimate for the number of barnacles.
countingBarnacles_circles.py was my first attempt and countingBarnacles_ovals.py was my second attempt (slightly more accurate than the first)

The images folder contains the results of the two main code files (centralCrop.py and countingBarnacles.py) being run on all possible provided images.
My code creates cropped images with the prefix "cropped_". It also creates masks (blue outline on black background) with prefix "mask_cropped_".
It also creates masked images (the original image with the mask overlayed on top) with prefix "masked_cropped_".
Note that the rest of the images (img1.png, img2.png, mask1.png, mask2.png, masked_img1.png, masked_img2.png, and unseen_img1.png) were source images provided for this project by DALI.

## __For centralCrop.py, the workflow is as follows:__

Allow the user to choose an imgName (name of the original image)

Load the image and convert it to the HSV (Hue, Saturation, Value) colorspace
- I decided to use HSV because for these images which are subject to varying lighting conditions, I can simply account for this by modifying the value (brightness) of my color. 
- Meanwhile, for the RGB color space, the intensity of the color is largely determined by lighting conditions. HSV is much more intuitive.
  
Create two variables to represent lower and upper bounds (in HSV) for the color green. Notice how I let Value range from 20 to 255 to account for varying lighting conditions, as explained above

Create a green mask (binary image) based on these lower and upper bounds for green.
- Every pixel in the image that is in the range of lower to upper bound is made white (color value 255) while everything else is made black (color value 0)
Apply morphological operations to “clean” debris from the mask
- I apply a combination of erosion and dilation
- Erosion: shrinking white regions - this effectively removes small white regions (noise)
- Dilation (restores larger white areas back to original size)
  
Extract the regions that are green and store them in the variable green_only
Then convert the image to grayscale and store in the variable green_gray:
- The result green_gray will be black for all regions not approximately green and varying levels of gray for the green regions
Apply adaptive thresholding on green_gray:
- The point of adaptive thresholding is that it calculates threshold values for small regions which means it does a better job of accounting for varying lighting conditions that normal thresholding which is strictly binary for one constant threshold
- The point of creating green_gray and only THEN applying adaptive thresholding is to ensure that adaptive thresholding is applied to approximately green regions, not the entire image where the adaptive threshold might be too soft
  
Extract contours using the adaptive threshold

Filter contours by area
Then I loop through each contour in my filtered_contours list and find the one which has an aspect ratio greater than 0.95 with the largest area:
- This essentially means finding the contour that is closest in shape to a square AND has the largest area
- This always results in largestContour being the outline for the central green/blue square
  
Finally I crop the image based on the bounding box of the largestContour and write it to my images folder.

## __For countingBarnacles_customkernel.py, the workflow is as follows:__

Allow the user to choose a cropped_img_name (name of the original image)

Load the image and convert it to GRAY
- The purpose of converting to gray is that canny edge detection generally works more effectively on grayscale rather than color images
  
Apply gaussian blur to the image:
- This helps to smooth out the image to reduce noise and excessive detail
  
Apply Canny edge detection:
- This helps to identify the edges in the grayscale image which will likely correspond to the barnacles we are trying to count
  
Apply further morphological operations to refine the edge detection:
- The goal is to remove noise and close gaps
- Apply MORPH_CLOSE, which is first dilation to expand the barnacles and then erosion which will fill small holes or gaps in the outlines of the barnacles
  
Extract contours

Create a black background to draw the contours on:
- This will be the eventual mask
Loop through each contour in contours:
- If the area is greater than 115 and the contour has at least 5 points, it can likely fit an ellipse
- So fit the ellipse and calculate its aspect ratio and circularity
- Filter based on aspect ratio and circularity: draw the filtered contours in blue on the black background
  
Output the number of barnacles detected to the terminal

Display the masked original image on top; to see just the mask simply move the top image to the right and look to the left.

## Conclusion: Model Performance + What I learned

I am thrilled with the performance of my centralCrop.py script, as it works perfectly for all provided images (img1.png, img2.png, and unseen_img1.png). This one took me a long time to work through, but going through openCV documentation and learning about the fact that using adaptive thresholding would be useful to account for different lighting conditions and create a binary image helped me in coming up with this solution. I learned all about openCV in python and set up VSCode (I was used to IntelliJ for Java) and learned about pushing code to GitHub and creating a Personal Access Token. 

Regarding my countingBarnacles_ files, the order in which I did them was circles, ovals, and finally customkernel. The accuracy of my code increased with each new iteration I made. For circles, I learned about the cv.HoughCircles method. For ovals, I simply applied edge detection and checked for properties of my contours. I did something similar but in a better way for my customkernel (better in that I used a Morphological kernel in the shape of an ellipse and used MORPH_CLOSE to solidify potential barnacle edges). 

Regarding performance: countingBarnacles_customkernel works extremely for img1 and unseen_img1, it works a little less better for img2 and unseen_img2 (reasoning: for img2 the lighting and colors are much different and for unseen_img2 the sample size is small). I'm not sure of the exact count of barnacles, but from an ad hoc view, I believe accuracy for img 1 and unseen_img1 is > 90% and for img2 and unseen_img2 it is > 70%!

In general, I learned about basic functions in openCV: cv.imshow, cv.waitKey, cv.imwrite. And I also learned and became fond of bounding boxes, which bound contours and allow you to compute very useful properties of the contours!

I am excited about all I have learned about python, openCV, GitHub, and VSCode, and think this project greatly enhanced my technical skills.


