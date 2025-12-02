import os
import cv2 as cv
import matplotlib.pyplot as plt
import argparse
import glob


def plot_image_thresholds(filename, threshold):
    # Build full path to images folder relative to script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, "images")

    if filename is None:
        # Find all image files in the folder
        image_files = glob.glob(os.path.join(images_dir, "*.*"))
        if not image_files:
            print("No images found in the 'images' folder.")
            return
        # Pick the most recently modified image
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

    # Plot grayscale histogram
    hist = cv.calcHist([imgGray], [0], None, [256], [0, 256])
    plt.figure()
    plt.plot(hist)
    plt.xlabel('Bins')
    plt.ylabel('# of pixels')
    plt.title('Grayscale Histogram')
    plt.show()

    # Threshold types
    thresOpt = [
        cv.THRESH_BINARY,
        cv.THRESH_BINARY_INV,
        cv.THRESH_TOZERO,
        cv.THRESH_TOZERO_INV,
        cv.THRESH_TRUNC
    ]
    thresNames = [
        'Binary',
        'BinaryInv',
        'ToZero',
        'ToZeroInv',
        'Trunc'
    ]

    # Plot original grayscale image
    plt.figure(figsize=(10, 5))
    plt.subplot(2, 3, 1)
    plt.imshow(imgGray, cmap='gray')
    plt.title('Original')
    plt.axis('off')

    # Apply and plot each threshold
    for i in range(len(thresOpt)):
        plt.subplot(2, 3, i+2)
        _, imgThres = cv.threshold(imgGray, threshold, 255, thresOpt[i])
        plt.imshow(imgThres, cmap='gray')
        plt.title(thresNames[i])
        plt.axis('off')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Plot image and threshold results.")
    parser.add_argument("--threshold", type=int, help="Threshold value (0-255)")
    parser.add_argument("--filename", type=str, default=None,
                        help="Image filename in the 'images' folder (default: most recent image)")
    args = parser.parse_args()

    plot_image_thresholds(filename=args.filename, threshold=args.threshold)
