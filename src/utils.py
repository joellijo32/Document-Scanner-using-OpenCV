import numpy as np
import cv2

def blank(shape, dtype=np.uint8, filler="0"):
    if filler == "0":
        blank = np.zeros(shape, dtype)
    elif filler == "1":
        blank = np.ones(shape, dtype)
    else:
        return "BAD FILLER VALUE; MUST BE STRINGS OF '0' OR '1'"

    return blank


def simple_erode(img):
    ekernel = np.ones((3, 3), np.uint8)
    eroded = cv2.erode(img, ekernel, iterations=1)

    return eroded


def simple_dilate(img):
    dkernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(img, dkernel, iterations=1)

    return dilated


def brightness_contrast(img, mult, add):
    adjusted = cv2.convertScaleAbs(img, alpha=float(mult), beta=float(add))

    return adjusted


def resize(img, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = img.shape[:2]

    if width is None and height is None:
        return img

    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    resized = cv2.resize(img, dim, interpolation=inter)

    return resized


def getoutlines(img):
    outlines = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
    return outlines


def order_points(pts):
    if str(type(pts)) != "<class 'numpy.ndarray'>":
        pts = np.array(pts)

    corners = np.zeros((4, 2), dtype="float32")

    sums = pts.sum(axis=1)
    corners[0] = pts[np.argmin(sums)]
    corners[2] = pts[np.argmax(sums)]

    diffs = np.diff(pts, axis=1)
    corners[1] = pts[np.argmin(diffs)]
    corners[3] = pts[np.argmax(diffs)]

    return corners


def perspective_transform(img, pts):
    corners_old = order_points(pts)
    tl, tr, br, bl = corners_old

    distT = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    distB = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    maxW = max(int(distT), int(distB))

    distL = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    distR = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    maxH = max(int(distL), int(distR))

    corners_corrected = np.array(
        [[0, 0], [maxW - 1, 0], [maxW - 1, maxH - 1], [0, maxH - 1]], dtype="float32"
    )

    matrix = cv2.getPerspectiveTransform(corners_old, corners_corrected)
    img_corrected = cv2.warpPerspective(img, matrix, (maxW, maxH))

    return img_corrected
