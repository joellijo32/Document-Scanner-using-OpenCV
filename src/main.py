import cv2

def main():
    print("OpenCV Template Running...")
    img = cv2.imread('assets/input/sample.jpg')
    if img is None:
        print("No sample image found.")
    else:
        cv2.imshow("Sample", img)
        cv2.waitKey(0)

if __name__ == "__main__":
    main()
