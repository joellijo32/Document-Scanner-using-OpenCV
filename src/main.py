import cv2
import argparse

from utils import resize
from utils import perspective_transform
from utils import getoutlines
from utils import simple_erode
from utils import simple_dilate
from utils import brightness_contrast
from utils import blank


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


if img is None:
    print()
    print("The file does not exist or is empty!")
    print("Please select a valid image file!")
    print()
    exit(0) 


def preprocess(img):
    img_adj = brightness_contrast(img, 1.56, -60)
    scale = img_adj.shape[0] / 500.0
    img_scaled = resize(img_adj, height=500)
    img_gray = cv2.cvtColor(img_scaled, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.GaussianBlur(img_gray, (11, 11), 0)
    img_edge = cv2.Canny(img_gray, 60, 245)
    img_edge = simple_dilate(img_edge)

    return img_adj, scale, img_scaled, img_edge


def gethull(img_edge):
    img_prehull = img_edge.copy()
    outlines = getoutlines(img_prehull)
    img_hull = blank(img_prehull.shape, img_prehull.dtype, "0")

    for outline in range(len(outlines)):
        hull = cv2.convexHull(outlines[outline])
        cv2.drawContours(img_hull, [hull], 0, 255, 3)

    img_hull = simple_erode(img_hull)

    return img_hull


def getcorners(img_hull):
    img_outlines = img_hull.copy()
    outlines = getoutlines(img_outlines)
    outlines = sorted(outlines, key=cv2.contourArea, reverse=True)[:4]

    for outline in outlines:
        perimeter = cv2.arcLength(outline, True)
        approx = cv2.approxPolyDP(outline, 0.02 * perimeter, True)

        if len(approx) == 4:
            corners = approx
            break

    return corners


img_adj, scale, img_scaled, img_edge = preprocess(img)
img_hull = gethull(img_edge)
corners = getcorners(img_hull)
corners = corners.reshape(4, 2) * scale
img_corrected = perspective_transform(img_adj, corners)
cv2.imwrite("./corrected.png", img_corrected)
img_corrected = cv2.cvtColor(img_corrected, cv2.COLOR_BGR2GRAY)

if args["inverted"] is not None:
    img_thresh = cv2.threshold(img_corrected, 135, 255, cv2.THRESH_BINARY_INV)[1]
    cv2.imwrite("./thresholded_inverted.png", img_thresh)
else:
    img_thresh = cv2.threshold(img_corrected, 135, 255, cv2.THRESH_BINARY)[1]
    cv2.imwrite("./thresholded.png", img_thresh)
