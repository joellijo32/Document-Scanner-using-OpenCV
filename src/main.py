import cv2
import argparse
import os

from utils import resize
from utils import perspective_transform
from utils import getoutlines
from utils import simple_erode
from utils import simple_dilate
from utils import brightness_contrast
from utils import blank

# Set up argument parser for command line arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    "-i", "--image", required=True, help="Path to the image to be corrected."
)
ap.add_argument(
    "-I",
    "--inverted",
    required=False,
    nargs="?",
    const="Ture",
    help="Invert the output if this argument present.",
)
args = vars(ap.parse_args())


img = cv2.imread(args["image"])

# Check if image is loaded successfully
if img is None:
    print()
    print("The file does not exist or is empty!")
    print("Please select a valid image file!")
    print()
    exit(0) 


def preprocess(img):
    """
    
    Adjusts brightness/contrast, resizes, converts to grayscale, blurs, and finds edges.
    """
  
    img_adj = brightness_contrast(img, 1.56, -60)
    
    
    scale = img_adj.shape[0] / 500.0

    img_scaled = resize(img_adj, height=500)
    
    img_gray = cv2.cvtColor(img_scaled, cv2.COLOR_BGR2GRAY)
    
    img_gray = cv2.GaussianBlur(img_gray, (11, 11), 0)
    
   
    img_edge = cv2.Canny(img_gray, 60, 245)
    
    
    img_edge = simple_dilate(img_edge)

    return img_adj, scale, img_scaled, img_edge


def gethull(img_edge):
    """
    Finds the convex hull of the edges.
    """
    img_prehull = img_edge.copy()
    outlines = getoutlines(img_prehull)
    
  
    img_hull = blank(img_prehull.shape, img_prehull.dtype, "0")

    for outline in range(len(outlines)):
      
        hull = cv2.convexHull(outlines[outline])
        # Draw the hull
        cv2.drawContours(img_hull, [hull], 0, 255, 3)

    # Erode the hull to refine the shape
    img_hull = simple_erode(img_hull)

    return img_hull


def getcorners(img_hull):
    """
    Finds the 4 corners of the document from the hull image.
    """
    img_outlines = img_hull.copy()
    outlines = getoutlines(img_outlines)
    
    
    outlines = sorted(outlines, key=cv2.contourArea, reverse=True)[:4]

    corners = None
    for outline in outlines:
     
        perimeter = cv2.arcLength(outline, True)
     
        approx = cv2.approxPolyDP(outline, 0.02 * perimeter, True)

        # If the polygon has 4 points, we assume it's our document
        if len(approx) == 4:
            corners = approx
            break

    return corners




img_adj, scale, img_scaled, img_edge = preprocess(img)

img_hull = gethull(img_edge)


corners = getcorners(img_hull)

# Check if corners were found
if corners is None:
    print("Could not find the document corners. Please try a different image.")
    exit(1)


corners = corners.reshape(4, 2) * scale


img_corrected = perspective_transform(img_adj, corners)

# Ensure results directory exists
if not os.path.exists("./results"):
    os.makedirs("./results")


cv2.imwrite("./results/corrected.png", img_corrected)

# Convert to grayscale
img_corrected = cv2.cvtColor(img_corrected, cv2.COLOR_BGR2GRAY)

# Apply inversion if requested, otherwise save grayscale
if args["inverted"] is not None:
  
    img_final = cv2.bitwise_not(img_corrected)
    cv2.imwrite("./results/scanned_inverted.png", img_final)
else:
  
    cv2.imwrite("./results/scanned.png", img_corrected)

print("Processing complete. Results saved in ./results/")

