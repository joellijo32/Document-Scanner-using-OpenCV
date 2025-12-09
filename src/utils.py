import numpy as np
import cv2

def blank(shape, dtype=np.uint8, filler="0"):
    """
    Creates a blank image (numpy array) filled with either 0s or 1s.

    """
    if filler == "0":
        blank = np.zeros(shape, dtype)
    elif filler == "1":
        blank = np.ones(shape, dtype)
    else:
        return "BAD FILLER VALUE; MUST BE STRINGS OF '0' OR '1'"

    return blank


def simple_erode(img):
    """
    Applies a simple 3x3 erosion to the image.

    """
    ekernel = np.ones((3, 3), np.uint8)
    eroded = cv2.erode(img, ekernel, iterations=1)

    return eroded


def simple_dilate(img):
    """
    Applies a simple 3x3 dilation to the image.
   
    """
    dkernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(img, dkernel, iterations=1)

    return dilated


def brightness_contrast(img, mult, add):
    """
    Adjusts the brightness and contrast of an image.
    mult: Contrast control (1.0-3.0)
    add: Brightness control (0-100)
    """
    adjusted = cv2.convertScaleAbs(img, alpha=float(mult), beta=float(add))

    return adjusted


def resize(img, width=None, height=None, inter=cv2.INTER_AREA):
    """
    Resizes the image while maintaining aspect ratio.
  
    """
    dim = None
    (h, w) = img.shape[:2]

    # If both are None, return original image
    if width is None and height is None:
        return img

    # Calculate aspect ratio
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    # Resize the image
    resized = cv2.resize(img, dim, interpolation=inter)

    return resized


def getoutlines(img):
    """
    Finds contours in the image.
    Returns a list of contours.
    """
    outlines = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
    return outlines


def order_points(pts):
    """
    Orders coordinates in the order: top-left, top-right, bottom-right, bottom-left.
    
    """
    if str(type(pts)) != "<class 'numpy.ndarray'>":
        pts = np.array(pts)

    corners = np.zeros((4, 2), dtype="float32")

    # Top-left will have the smallest sum, bottom-right will have the largest sum
    sums = pts.sum(axis=1)
    corners[0] = pts[np.argmin(sums)]
    corners[2] = pts[np.argmax(sums)]

    # Top-right will have the smallest difference, bottom-left will have the largest difference
    diffs = np.diff(pts, axis=1)
    corners[1] = pts[np.argmin(diffs)]
    corners[3] = pts[np.argmax(diffs)]

    return corners


def perspective_transform(img, pts):
    """
    Applies a 4-point perspective transform to obtain a top-down view of the image.
    """
    # Order the points first
    corners_old = order_points(pts)
    tl, tr, br, bl = corners_old

    # Calculate the width of the new image
    distT = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    distB = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    maxW = max(int(distT), int(distB))

    # Calculate the height of the new image
    distL = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    distR = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    maxH = max(int(distL), int(distR))

    # Construct the set of destination points
    corners_corrected = np.array(
        [[0, 0], [maxW - 1, 0], [maxW - 1, maxH - 1], [0, maxH - 1]], dtype="float32"
    )

    # Compute the perspective transform matrix and apply it
    matrix = cv2.getPerspectiveTransform(corners_old, corners_corrected)
    img_corrected = cv2.warpPerspective(img, matrix, (maxW, maxH))

    return img_corrected
