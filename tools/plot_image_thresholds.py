import os
import cv2 as cv
import matplotlib.pyplot as plt
import argparse
import glob
import math
import numpy as np


def plot_image_thresholds(filename, threshold):
    # Build full path to images folder relative to script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, "images")

    if filename is None:
        image_files = glob.glob(os.path.join(images_dir, "*.*"))
        if not image_files:
            print("No images found in the 'images' folder.")
            return
        image_path = max(image_files, key=os.path.getmtime)
        print(
            f"No filename given. Using most recent image: {os.path.basename(image_path)}")
    else:
        image_path = os.path.join(images_dir, filename)
        if not os.path.exists(image_path):
            print(f"Image '{filename}' not found in images folder.")
            return

    img = cv.imread(image_path)
    if img is None:
        print(f"Failed to load image '{os.path.basename(image_path)}'.")
        return

    # Blur first
    imgBlur = cv.GaussianBlur(img, (5, 5), 0)

    # Convert to HSV and create mask
    hsv = cv.cvtColor(imgBlur, cv.COLOR_BGR2HSV)
    lower_red = np.array([0, 50, 225]) # Filter for whitish red flash
    upper_red = np.array([10, 200, 255])
    mask_red = cv.inRange(hsv, lower_red, upper_red)

    # Apply mask to blurred BGR image
    imgMasked = cv.bitwise_and(imgBlur, imgBlur, mask=mask_red)

    # Convert to grayscale for thresholding
    imgGray = cv.cvtColor(imgMasked, cv.COLOR_BGR2GRAY)

    # Plot grayscale histogram
    hist = cv.calcHist([imgGray], [0], None, [256], [0, 256])
    plt.figure()
    plt.plot(hist)
    plt.xlabel('Bins')
    plt.ylabel('# of pixels')
    plt.title('Grayscale Histogram')
    plt.show()

    # Threshold types
    thresholds = [
        threshold,
        threshold,
        threshold,
        threshold,
        threshold,
        0,
    ]
    thresOpt = [
        cv.THRESH_BINARY,
        cv.THRESH_BINARY_INV,
        cv.THRESH_TOZERO,
        cv.THRESH_TOZERO_INV,
        cv.THRESH_TRUNC,
        cv.THRESH_BINARY + cv.THRESH_OTSU,  # Attempts to separate foreground/background
    ]
    thresNames = [
        'Binary',
        'BinaryInv',
        'ToZero',
        'ToZeroInv',
        'Trunc',
        'Otsu',
    ]

    total_images = 1 + len(thresOpt)   # 1 = original image
    cols = 3
    rows = math.ceil(total_images / cols)

    plt.figure(figsize=(12, rows * 4))

    # Plot original
    plt.subplot(rows, cols, 1)
    plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    plt.title('Original')
    plt.axis('off')

    # Apply and plot each threshold
    imgGrayMasked = cv.cvtColor(imgMasked, cv.COLOR_BGR2GRAY)  # use imgMasked instead of img_red
    for i, (name, opt, thres) in enumerate(zip(thresNames, thresOpt, thresholds)):
        pos = i + 2
        _, timg = cv.threshold(imgGrayMasked, thres, 255, opt)
        plt.subplot(rows, cols, pos)
        plt.imshow(timg, cmap='gray')
        plt.title(name)
        plt.axis('off')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Plot image and threshold results.")
    parser.add_argument("--threshold", type=int,
                        help="Threshold value (0-255)")
    parser.add_argument("--filename", type=str, default=None,
                        help="Image filename in the 'images' folder (default: most recent image)")
    args = parser.parse_args()

    plot_image_thresholds(filename=args.filename, threshold=args.threshold)
