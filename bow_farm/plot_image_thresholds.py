import os
import cv2 as cv
import matplotlib.pyplot as plt
import argparse
import glob
import math


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

    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray, (5, 5), 0)  # Reduces image noise
    # imgBlur = cv.medianBlur(imgGray, 5)

    # Plot grayscale histogram
    hist = cv.calcHist([imgBlur], [0], None, [256], [0, 256])
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
    plt.imshow(imgBlur, cmap='gray')
    plt.title('Original')
    plt.axis('off')

    # Plot thresholded images
    for i, (name, opt, thres) in enumerate(zip(thresNames, thresOpt, thresholds)):
        pos = i + 2  # shift by 1 for original image
        _, timg = cv.threshold(imgBlur, thres, 255, opt)

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
